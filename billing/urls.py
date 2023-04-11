from django.contrib.auth import views as auth_views
from django.urls import path

from billing import views

app_name = 'billing'
urlpatterns = [
    path('', views.index, name='index_no_number'),
    path('<int:table_number>/', views.index, name='index'),
]
