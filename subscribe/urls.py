from django.urls import path
from subscribe import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profileupdate', views.profile_update, name='profile_update')
]