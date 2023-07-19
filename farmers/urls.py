from django.conf import settings
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
 

urlpatterns = [
    path('' ,views.farmer, name='farmer'),
     path('profile/<username>/', views.profile, name='profile'),
    path('learn', views.learn, name='learn'),
    path('user_profile/<username>/', views.user_profile, name='user_profile'),
    path('new/status/<username>', views.new_status, name='newStatus'),
    path('post/<id>', views.post_comment, name='comment'),
    path('search/', views.search_profile, name='search'),
    path('unfollow/<to_unfollow>', views.unfollow, name='unfollow'),
    path('follow/<to_follow>', views.follow, name='follow'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)