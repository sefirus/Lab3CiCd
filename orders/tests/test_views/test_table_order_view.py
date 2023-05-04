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


@pytest.mark.django_db
def test_table_order_get_multiple_personal_orders(client: Client, table_order, person_1, person_2, person_3,
                                                  menu_item_1, menu_item_2, menu_item_3):
    po1 = PersonalOrder.objects.create(table_order=table_order, person=person_1,
                                       total=menu_item_1.price + menu_item_2.price + menu_item_3.price)
    po1.items.set([menu_item_1, menu_item_2, menu_item_3])

    po2 = PersonalOrder.objects.create(table_order=table_order, person=person_2,
                                       total=menu_item_1.price + menu_item_3.price)
    po2.items.set([menu_item_1, menu_item_3])

    po3 = PersonalOrder.objects.create(table_order=table_order, person=person_3,
                                       total=menu_item_2.price + menu_item_3.price)
    po3.items.set([menu_item_2, menu_item_3])

    table_order.personal_orders.set([po1, po2, po3])

    path = reverse('orders:table_order', args=[table_order.id, po1.id])
    response = client.get(path)

    assert response.status_code == 200
    assert response.context['selected_personal_order'] == po1
    assert response.context['total'] == po1.total

    selected_menu_items = response.context['selected_menu_items']
    assert len(selected_menu_items) == 3
    assert menu_item_1 in selected_menu_items
    assert menu_item_2 in selected_menu_items
    assert menu_item_3 in selected_menu_items
