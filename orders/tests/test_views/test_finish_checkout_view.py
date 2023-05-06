import uuid

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from orders.models import TableOrder


@pytest.mark.django_db
def test_finish_checkout_success(client, table_order):
    path = reverse('orders:finish_checkout', args=[table_order.id])
    response = client.post(path)

    table_order.refresh_from_db()
    assert response.status_code == 302
    assert response.url == reverse('employees:waiter_home')
    assert table_order.status == 'Accepted'


@pytest.mark.django_db
def test_finish_checkout_nonexistent_table_order(client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')

    non_existent_table_order_id = uuid.uuid4()
    path = reverse('orders:finish_checkout', args=[non_existent_table_order_id])
    response = client.post(path)

    assert response.status_code == 404