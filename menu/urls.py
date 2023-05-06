from django.contrib.auth import views as auth_views
from django.urls import path

from menu import views

app_name = 'menu'
urlpatterns = [
    path('<int:id>/', views.menu, name='menu'),
]