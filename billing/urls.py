from django.urls import path

from billing import views


app_name = 'billing'
urlpatterns = [
    path('', views.index, name='index_no_number'),
    path('<int:table_number>/', views.index, name='index'),
    path('call_waiter/', views.call_waiter, name='call_waiter'),
    path('client_checkout/<int:table_number>', views.client_checkout, name='client_checkout'),
    path("payment/<uuid:group_order_id>/", views.payment, name="payment"),
]
