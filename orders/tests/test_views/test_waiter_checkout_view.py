import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_waiter_checkout_group_order(client: Client, table_order, personal_order_1, personal_order_2, group_order_1):
    personal_order_1.parent_group_order = group_order_1
    personal_order_1.save()
    personal_order_2.parent_group_order = group_order_1
    personal_order_2.save()

    path = reverse('orders:checkout', args=[table_order.id])
    response = client.get(path)

    assert response.status_code == 200

    context = response.context
    assert context['table_order'] == table_order
    assert context['unprocessed_personal_orders'].count() == 0
    assert context['group_orders'].count() == 1

    group_order = context['group_orders'][0]
    assert group_order.total == (personal_order_1.total + personal_order_2.total)
    assert personal_order_1.person.title in group_order.title
    assert personal_order_2.person.title in group_order.title
