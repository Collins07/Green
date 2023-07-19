from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('' ,views.home, name='home'),
    path('about' ,views.about, name='about'),
    path('reforest' ,views.index, name='reforest'),
    path('greenspace' ,views.greenspace, name='greenspace'),
    path('add_trees' ,views.add_trees, name='add_trees'),
    path('edit_trees/<int:id>' ,views.reforest_edit, name='reforest-edit'),
    path('delete_trees/<int:id>' ,views.reforest_delete, name='reforest-delete'),
    path('search-reforest' , csrf_exempt(views.search_reforest), name='search_reforest'),
    path('reforest_category_summary', views.reforest_category_summary, 
         name="reforest_category_summary"),
    path ('stats', views.stats, name='stats'),
    path ('export_csv_reforest/', views.export_csv_reforest, name='export-csv-reforest'),
    path ('export_pdfs/', views.export_pdfs, name='export-pdfs'),
    
     

]