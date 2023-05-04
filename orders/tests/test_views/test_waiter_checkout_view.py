import pytest
from django.test import Client
from django.urls import reverse

from orders.models import GroupOrder


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


@pytest.mark.django_db
def test_waiter_checkout_three_group_orders_one_po_each(
        client: Client, table_order, personal_order_1, personal_order_2, personal_order_3, menu_item_1
):
    personal_orders = [personal_order_1, personal_order_2, personal_order_3]
    for po in personal_orders:
        po.items.add(menu_item_1)
        po.total = menu_item_1.price
        po.save()
        go = GroupOrder.objects.create(table_order=table_order)
        go.personal_orders.add(po)

    path = reverse('orders:checkout', args=[table_order.id])
    response = client.get(path)

    assert response.status_code == 200

    group_orders = response.context['group_orders']
    assert len(group_orders) == 3

    for go in group_orders:
        assert len(go.personal_orders.all()) == 1
        assert go.total == menu_item_1.price


@pytest.mark.django_db
def test_waiter_checkout_three_group_orders_different_po_counts(
        client: Client, table_order, personal_order_1, personal_order_2, personal_order_3, personal_order_4,
        personal_order_5, menu_item_1
):
    personal_orders = [personal_order_1, personal_order_2, personal_order_3, personal_order_4, personal_order_5]
    for po in personal_orders:
        po.items.add(menu_item_1)
        po.total = menu_item_1.price
        po.save()

    go1 = GroupOrder.objects.create(table_order=table_order)
    go1.personal_orders.add(personal_order_1, personal_order_2)

    go2 = GroupOrder.objects.create(table_order=table_order)
    go2.personal_orders.add(personal_order_3, personal_order_4)

    go3 = GroupOrder.objects.create(table_order=table_order)
    go3.personal_orders.add(personal_order_5)

    path = reverse('orders:checkout', args=[table_order.id])
    response = client.get(path)

    assert response.status_code == 200

    group_orders = response.context['group_orders']
    assert len(group_orders) == 3

    go1_response = group_orders.get(id=go1.id)
    assert len(go1_response.personal_orders.all()) == 2

    go2_response = group_orders.get(id=go2.id)
    assert len(go2_response.personal_orders.all()) == 2

    go3_response = group_orders.get(id=go3.id)
    assert len(go3_response.personal_orders.all()) == 1
