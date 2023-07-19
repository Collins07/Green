from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('' ,views.forest, name='forest'),
    path('add_forest' ,views.add_forest, name='add_forest'),
     path('search-forest' , csrf_exempt(views.search_forest), name='search_forest'),
     path('search-difference' , csrf_exempt(views.search_difference), name='search_difference'),
     path ('export_csv', views.export_csv, name='export-csv'),
     path ('export_pdf', views.export_pdf, name='export-pdf'),
     path ('export_difference_pdf', views.export_difference_pdf, name='export-difference-pdf'),
    path ('trend', views.difference, name='trend'),


]