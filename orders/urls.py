from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # other URL patterns ...
    path('create-table-order/', views.create_table_order, name='create_table_order'),
    path('table_order/<uuid:table_order_id>/', views.table_order, name='table_order'),
    path('table_order/<uuid:table_order_id>/<uuid:personal_order_id>/', views.table_order, name='table_order'),
    path('table_order/<uuid:table_order_id>/create_personal_order/', views.create_personal_order,
         name='create_personal_order'),
    path('table_order/<uuid:table_order_id>/<uuid:personal_order_id>/add_menu_item/', views.add_menu_item,
         name='add_menu_item'),
    path('table_order/<uuid:table_order_id>/checkout/', views.waiter_checkout, name='checkout'),
    path('table_order/<uuid:table_order_id>/create_group_order/', views.create_group_order, name='create_group_order'),
    path('table_order/<uuid:table_order_id>/finish_checkout/', views.finish_checkout, name='finish_checkout'),
]
