from django.urls import path
from temple import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('userpage/', views.user_page, name='userpage'),
    path('panteon/', views.panteon, name='panteon'),
    path('creategod/', views.create_god, name='creategod'),
]