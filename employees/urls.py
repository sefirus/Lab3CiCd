from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    path('home/', views.waiter_home, name='waiter_home'),
    path('login/', views.waiter_login, name='waiter_login')
]
