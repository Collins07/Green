from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.csrf import csrf_exempt



urlpatterns = [
    path('susbscribe', views.carbon, name="carbon"),
    path('benefits', views.benefits, name="benefits"),
     
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)