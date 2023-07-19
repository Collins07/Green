from django.shortcuts import render

# Create your views here.
def carbon(request):
    return render (request, 'carbon/index.html')

def benefits(request):
    return render (request, 'carbon/benefits.html')