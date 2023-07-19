from pyexpat import model
from django.conf import settings
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required,permission_required
from .models import Category, Reforest
from django.contrib import messages
from django.core.paginator import Paginator
import json
import datetime
import csv
from django.db.models import Sum

from xhtml2pdf import pisa
from io import BytesIO

from django.template.loader import render_to_string, get_template



# Create your views here.
def search_reforest(request):
    if request.method == 'POST':
      search_str=json.loads(request.body).get('searchText')
      reforests = Reforest.objects.filter(
          trees_planted__istartswith=search_str) | Reforest.objects.filter(
          date__istartswith=search_str) | Reforest.objects.filter(
          description__icontains=search_str) | Reforest.objects.filter(
          category__icontains=search_str)
      data = reforests.values()
      return JsonResponse(list(data), safe=False)



def index(request):
    
    reforest = Reforest.objects.order_by('-date')
    total_trees = reforest.aggregate(total_trees_planted=Sum('trees_planted'))['total_trees_planted']

    highest_entry = reforest.order_by('-trees_planted').first()
    highest_group = highest_entry.description if highest_entry else None


    

    paginator=Paginator(reforest, 4)
    page_number = request.GET.get('page')
    page_obj= Paginator.get_page(paginator,page_number)

    
    context = {
        'reforest': reforest,
        'page_obj': page_obj,
        'total_trees': total_trees,
        'highest_group': highest_group,
        'paginator': paginator
      

    }
    return render(request, 'reforest/index.html', context)


def add_trees(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST,
    }
    
    if request.method == 'POST':
        trees_planted = request.POST['trees_planted']
        description = request.POST['description']
        date_str = request.POST['date']
        category = request.POST['category']

        if not trees_planted:
            messages.error(request, 'Number of trees planted is required!')
            return render(request, 'reforest/add_trees.html', context)

        if not description:
            messages.error(request, 'The name of your group is required!')
            return render(request, 'reforest/add_trees.html', context)

        # Parse date string into date object
        try:
            parsed_date = datetime.date.fromisoformat(date_str)
        except ValueError:
            messages.error(request, 'Invalid date format. Please provide a valid date.')
            return render(request, 'reforest/add_trees.html', context)

        # Check if the date is in the future
        if parsed_date > datetime.date.today():
            messages.error(request, 'Invalid date. Please select a past or today\'s date.')
            return render(request, 'reforest/add_trees.html', context)

        Reforest.objects.create(owner=request.user, trees_planted=trees_planted, description=description, date=parsed_date, category=category)
        messages.success(request, 'Data saved successfully')

        return redirect('reforest')

    return render(request, 'reforest/add_trees.html', context)


def home(request):
    return render(request, 'reforest/home.html')


def about(request):
    return render(request, 'reforest/about.html')



def reforest_edit(request, id):
    reforest = Reforest.objects.get(pk=id)
    categories = Category.objects.all()

    context = {
        'reforest': reforest,
        'values': reforest,
        'categories': categories
    }
    if request.method == 'GET':
        
        return render(request, 'reforest/edit_trees.html', context)
    if request.method == 'POST':
        trees_planted = request.POST['trees_planted']

        if not trees_planted:
            messages.error(request,'Number of trees planted required !!!')
            return render(request, 'reforest/edit_trees.html', context)
        description = request.POST['description']
        date = request.POST['date']
        category = request.POST['category']
        
    if request.method == 'POST':
        description = request.POST['description']

        if not description:
            messages.error(request,' The name of your group is required !!!')
            return render(request, 'reforest/edit_trees.html', context)
        

        reforest.owner=request.user
        reforest.trees_planted=trees_planted
        reforest.description=description
        reforest.date=date
        reforest.category=category

        reforest.save()
        messages.success(request, 'Your data has been updated successfully')

        return redirect('index')



def reforest_delete(request,id):
    reforest = Reforest.objects.get(pk=id)
    reforest.delete()
    messages.error(request, 'Your data has been deleted')
    return redirect('index')


def reforest_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago= todays_date - datetime.timedelta(days=30*12)
    reforests = Reforest.objects.all()
    finalrep  = {}

    def get_category(reforest):
        return reforest.category
    
    category_list= list(set(map(get_category, reforests)))

    def get_reforest_category_trees_planted(category):
        trees_planted=0
        filtered_by_category = reforests.filter(category=category)

        for item in filtered_by_category:
            trees_planted += item.trees_planted

        return trees_planted

    for x in reforests:
        for y in category_list:
            finalrep[y] = get_reforest_category_trees_planted(y)



    return JsonResponse({"reforest_category_data": finalrep}, safe=False)   


def stats(request):
    return render (request, 'reforest/stats.html')

def export_csv_reforest(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition']= 'attachment; filename=Reforestation & Afforestation Records '+ str(datetime.datetime.now())+'.csv'

    writer = csv.writer(response)
    writer.writerow(['Group Name', 'Category', 'Trees Planted', 'Date'])

    reforest=Reforest.objects.all()

    for tree in reforest:
        writer.writerow([tree.description,
                         tree.category, tree.trees_planted, tree.date])
        
    return response 


def export_pdfs(request):
    reforest_entries = Reforest.objects.all()

    
    template = get_template('reforest/main_pdf_template.html')
    context = {'reforest_entries': reforest_entries}
    html = template.render(context)

    result = BytesIO()

    
    pisa.CreatePDF(html, dest=result)

    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Reforestation & Afforestation Report.pdf"'


    pdf = result.getvalue()
    response.write(pdf)

    return response



 
def greenspace(request):
    return render (request, 'reforest/greenspace.html')


