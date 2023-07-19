
from operator import itemgetter
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required,permission_required
from .models import Forest, Reason
from django.contrib import messages
from django.core.paginator import Paginator
# from .userpreferences.models import UserPrefrence
import json
from django.db.models import Sum
from django.http import Http404, JsonResponse, HttpResponse
import datetime
import csv
import base64
import os

from django.template.loader import render_to_string, get_template
from xhtml2pdf import pisa
from io import BytesIO
from dateutil import parser
from django.template import RequestContext
from django.conf import settings

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.db.models import F
from reforest.models import Reforest



# Create your views here.
def search_forest(request):
    if request.method == 'POST':
      search_str=json.loads(request.body).get('searchText')
      forest = Forest.objects.filter(
          trees_planted__istartswith=search_str) | Forest.objects.filter(
          date__istartswith=search_str) | Forest.objects.filter(
          description__icontains=search_str)
      data = forest.values()
      return JsonResponse(list(data), safe=False)




def forest(request):
    
    forest = Forest.objects.order_by('-date')
    total_trees = forest.aggregate(total_trees_planted=Sum('trees_planted'))['total_trees_planted']

    first_entry_trees = Reforest.objects.values('description').annotate(trees_planted=F('trees_planted')).order_by('description')
    second_entry_trees = forest.values('description').annotate(trees_planted=F('trees_planted')).order_by('description')

    highest_entry = forest.order_by('-trees_planted').first()
    highest_group = highest_entry.description if highest_entry else None

    diff_trees = []
    for first_entry in first_entry_trees:
        description = first_entry['description']
        first_entry_trees_planted = first_entry['trees_planted']
        second_entry = second_entry_trees.filter(description=description).first()
        if second_entry:
            second_entry_trees_planted = second_entry['trees_planted']
            diff_trees.append({
                'description': description,
                'trees_difference': second_entry_trees_planted - first_entry_trees_planted,
            })


    paginator=Paginator(forest, 4)
    page_number = request.GET.get('page')
    page_obj= Paginator.get_page(paginator,page_number)
    context = {
        'forest': forest,
        'page_obj': page_obj,
        'paginator': paginator,
        'total_trees': total_trees,
        'highest_group': highest_group,
         'diff_trees': diff_trees,

    }
    return render(request, 'forests/index.html', context)


def add_forest(request):
    reasons = Reason.objects.all()
    context = {
        'reasons': reasons,
        'values': request.POST,
    }

  
    
    if request.method == 'POST':
        trees_planted = request.POST['trees_planted']
        description = request.POST['description']
        date_str = request.POST['date']

        if not trees_planted:
            messages.error(request, 'Number of trees planted is required!')
            return render(request, 'forests/add_forest.html', context)

        if not description:
            messages.error(request, 'The name of your group is required!')
            return render(request, 'forests/add_forest.html', context)
        
        # Parse date string into date object
        try:
            parsed_date = datetime.date.fromisoformat(date_str)
        except ValueError:
            messages.error(request, 'Invalid date format. Please provide a valid date.')
            return render(request, 'forests/add_forest.html', context)

        # Check if the date is in the past or today
        if parsed_date > datetime.date.today():
            messages.error(request, 'Invalid date. Please select a past or today\'s date.')
            return render(request, 'forests/add_forest.html', context)


        Forest.objects.create(owner=request.user, trees_planted=trees_planted, description=description, date=parsed_date)
        messages.success(request, 'Data saved successfully')

        return redirect('forest')

    return render(request, 'forests/add_forest.html', context)



def forest_edit(request, id):
    forest = get_object_or_404(Forest, pk=id, owner=request.user)
    reasons = Reason.objects.all()

    context = {
        'forest': forest,
        'values': forest,
        'reasons': reasons
    }

    if request.method == 'GET':
        return render(request, 'forests/edit_forest.html', context)
    
    if request.method == 'POST':
        trees_planted = request.POST['trees_planted']
        description = request.POST['description']
        date = request.POST['date']

        if not trees_planted:
            messages.error(request, 'Number of trees planted is required!')
            return render(request, 'forests/edit_forest.html', context)

        if not description:
            messages.error(request, 'The name of your group is required!')
            return render(request, 'forests/edit_forest.html', context)

        forest.trees_planted = trees_planted
        forest.description = description
        forest.date = date

        forest.save()
        messages.success(request, 'Your data has been updated successfully')

        return redirect('forest')



def forest_delete(request,id):
    forest = Forest.objects.get(pk=id)
    forest.delete()
    messages.error(request, 'Your data has been deleted')
    return redirect('forest')


def export_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition']= 'attachment; filename=Reforestation & Afforestation Update Records '+ str(datetime.datetime.now())+'.csv'

    writer = csv.writer(response)
    writer.writerow(['Group Name', 'Trees Planted',  'Date'])

    forest=Forest.objects.all()

    for tree in forest:
        writer.writerow([ tree.description, tree.trees_planted, tree.date])
        
    return response 


def export_pdf(request):
   
    reforest_entries = Forest.objects.all()

   
    template = get_template('forests/pdf_template.html')
    context = {'reforest_entries': reforest_entries}
    html = template.render(context)

    
    result = BytesIO()

   
    pisa.CreatePDF(html, dest=result)

    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Reforestation & Afforestation Periodic updates.pdf"'

   
    pdf = result.getvalue()
    response.write(pdf)

    return response


def calculate_trees_difference(first_entry_trees, second_entry_trees):
    diff_trees = []
    for first_entry in first_entry_trees:
        description = first_entry['description']
        first_entry_trees_planted = first_entry['trees_planted']
        second_entries = second_entry_trees.filter(description=description).order_by('-date')
        if second_entries:
            second_entry = second_entries.first()
            second_entry_trees_planted = second_entry['trees_planted']
            difference = first_entry_trees_planted - second_entry_trees_planted 
            percentage = (second_entry_trees_planted/ first_entry_trees_planted) * 100
            diff_trees.append({
                'description': description,
                'percentage': round(percentage, 2),
                'trees_difference': difference,
            })
    return diff_trees



def difference(request):
    first_entry_trees = Reforest.objects.values('description').annotate(trees_planted=F('trees_planted')).order_by('description')
    second_entry_trees = Forest.objects.values('description').annotate(trees_planted=F('trees_planted')).order_by('description')

    diff_trees = calculate_trees_difference(first_entry_trees, second_entry_trees)
    
     # Sort the diff_trees list based on the percentage in descending order
    diff_trees = sorted(diff_trees, key=itemgetter('percentage'), reverse=True)

    paginator = Paginator(diff_trees,5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'diff_trees': page_obj,
        'paginator': paginator,
    }

    return render(request, 'forests/difference.html', context)


def search_difference(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        
        first_entry_trees = Reforest.objects.values('description').annotate(trees_planted=F('trees_planted')).order_by('description')
        second_entry_trees = Forest.objects.values('description').annotate(trees_planted=F('trees_planted')).order_by('description')

        diff_trees = calculate_trees_difference(first_entry_trees, second_entry_trees)

        # Filter the diff_trees list based on the search criteria
        filtered_trees = [tree for tree in diff_trees if search_str.lower() in tree['description'].lower()]

        # Sort the filtered_trees list based on the percentage in descending order
        filtered_trees = sorted(filtered_trees, key=itemgetter('percentage'), reverse=True)

        return JsonResponse(filtered_trees, safe=False)

    return JsonResponse([], safe=False)



def export_difference_pdf(request):
    # Get the difference between entries
    first_entry_trees = Reforest.objects.values('description').annotate(trees_planted=F('trees_planted')).order_by('description')
    second_entry_trees = Forest.objects.values('description').annotate(trees_planted=F('trees_planted')).order_by('description')
    diff_trees = calculate_trees_difference(first_entry_trees, second_entry_trees)
    diff_trees = sorted(diff_trees, key=itemgetter('percentage'), reverse=True)

    # Prepare the data for PDF template
    template = get_template('forests/difference_pdf.html')
    context = {'diff_trees': diff_trees, 'STATIC_URL': settings.STATIC_URL, 'HOST': request.META['HTTP_HOST']}
    html = template.render(context, request)

    # Generate PDF
    result = BytesIO()
    pisa.CreatePDF(html, dest=result)

    # Prepare and return the HTTP response with PDF attachment
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Accountability_Score.pdf"'
    pdf = result.getvalue()
    response.write(pdf)

    return response
