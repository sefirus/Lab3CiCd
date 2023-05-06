import pytest
import uuid
from django.test import Client
from django.urls import reverse

from orders.models import TableOrder


@pytest.mark.django_db
def test_create_table_order_success(client: Client, table_3):
    path = reverse('orders:create_table_order')
    response = client.get(path)
    assert response.status_code == 200

    form_data = {'table': table_3.id}
    response = client.post(path, data=form_data)

    assert response.status_code == 200  # Successful form submission should redirect to the waiter home page.
    assert TableOrder.objects.filter(table=table_3).exists()  # A table order should be created for table_3.


@pytest.mark.django_db
def test_create_table_order_invalid_table(client: Client):
    path = reverse('orders:create_table_order')
    response = client.get(path)
    assert response.status_code == 200

    invalid_table_id = uuid.uuid4()
    form_data = {'table': invalid_table_id}
    response = client.post(path, data=form_data)

    assert response.status_code == 200  # The page should not redirect, and the form should not be submitted.
    assert not TableOrder.objects.filter(table_id=invalid_table_id).exists()  # No table order should be created.


@pytest.mark.django_db
def test_create_table_order_empty_form(client: Client):
    path = reverse('orders:create_table_order')
    response = client.get(path)
    assert response.status_code == 200

    form_data = {}
    response = client.post(path, data=form_data)
    initial_table_orders_count = TableOrder.objects.count()

    assert response.status_code == 200  # The page should not redirect, and the form should not be submitted.
    assert TableOrder.objects.count() == initial_table_orders_count  # No table order should be created.
