import pytest
from django.test import Client
from django.urls import reverse

from orders.models import PersonalOrder


@pytest.mark.django_db
def test_add_menu_item_success(client: Client, table_order, person_1, menu_item_1):
    personal_order = PersonalOrder.objects.create(table_order=table_order, person=person_1, total=0)
    path = reverse('orders:add_menu_item', args=[table_order.id, personal_order.id])
    initial_total = personal_order.total

    response = client.post(path, {'menu_item': menu_item_1.id})

    personal_order.refresh_from_db()
    assert response.status_code == 302  # Successful form submission should redirect to the table order page.
    assert menu_item_1 in personal_order.items.all()
    assert personal_order.total == initial_total + menu_item_1.price

@pytest.mark.django_db
def test_add_menu_item_invalid_menu_item(client: Client, table_order, person_1):
    personal_order = PersonalOrder.objects.create(table_order=table_order, person=person_1, total=0)
    path = reverse('orders:add_menu_item', args=[table_order.id, personal_order.id])
    invalid_menu_item_id = 99999

    response = client.post(path, {'menu_item': invalid_menu_item_id})

    assert response.status_code == 400  # Invalid form submission should return a bad request response.

@pytest.mark.django_db
def test_add_menu_item_invalid_request_method(client: Client, table_order, person_1):
    personal_order = PersonalOrder.objects.create(table_order=table_order, person=person_1, total=0)
    path = reverse('orders:add_menu_item', args=[table_order.id, personal_order.id])

    response = client.get(path)

    assert response.status_code == 400  # Invalid request method should return a bad request response.
