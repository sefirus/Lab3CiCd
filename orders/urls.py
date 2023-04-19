from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # other URL patterns ...
    path('create-table-order/', views.create_table_order, name='create_table_order'),
]