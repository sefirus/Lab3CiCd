import pytest
from django.test import Client
from django.urls import reverse

from orders.models import PersonalOrder


@pytest.mark.django_db
def test_table_order_get_empty(table_order, client: Client):
    path = reverse('orders:table_order', args=[table_order.id])
    response = client.get(path)
    total = response.context['total']
    table_order_response = response.context['table_order']
    assert response.status_code == 200
    assert total == 0
    assert table_order_response.id == table_order.id


@pytest.mark.django_db
def test_table_order_get_one_empty_po(client: Client, table_order, person_1):
    po = PersonalOrder.objects.create(table_order=table_order, person=person_1, total=0)
    table_order.personal_orders.add(po)
    path = reverse('orders:table_order', args=[table_order.id, po.id])
    response = client.get(path)
    total = response.context['total']
    table_order_response = response.context['table_order']
    table_order_has_non_empty_personal_orders = response.context['table_order_has_non_empty_personal_orders']
    personal_orders = response.context['personal_orders']
    assert response.status_code == 200
    assert total == 0
    assert table_order_response.id == table_order.id
    assert table_order_has_non_empty_personal_orders is False
    assert len(personal_orders) == 1

