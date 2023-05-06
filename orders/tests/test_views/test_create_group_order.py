import pytest
from django.test import Client
from django.urls import reverse

from orders.models import GroupOrder, TableOrder


@pytest.mark.django_db
def test_create_group_order_with_two_personal_orders(client: Client, table_order, personal_order_1, personal_order_2):
    path = reverse('orders:create_group_order', args=[table_order.id])
    response = client.post(path, data={
        'personal_orders': [personal_order_1.id, personal_order_2.id]
    })
    assert response.status_code == 302
    group_orders = GroupOrder.objects.filter(table_order=table_order)
    assert group_orders.count() == 1
    group_order = group_orders.first()
    table_order = TableOrder.objects.filter(id=table_order.id).first()
    assert group_order.personal_orders.count() == 2
    assert personal_order_1 in group_order.personal_orders.all()
    assert personal_order_2 in group_order.personal_orders.all()
    assert table_order.status == 'Checkout In Progress'


@pytest.mark.django_db
def test_create_group_order_with_no_personal_orders(client: Client, table_order):
    path = reverse('orders:create_group_order', args=[table_order.id])
    response = client.post(path, data={})
    assert response.status_code == 302
    group_orders = GroupOrder.objects.filter(table_order=table_order)
    table_order = TableOrder.objects.filter(id=table_order.id).first()
    assert group_orders.count() == 0
    assert table_order.status != 'Checkout In Progress'
