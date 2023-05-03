import uuid
from django.urls import reverse, resolve


class TestUrls:
    def test_table_order_only_self_id_url(self):
        path = reverse('orders:table_order', args=[uuid.uuid4()])
        assert resolve(path).view_name == 'orders:table_order'

    def test_table_order_only_personal_url(self):
        path = reverse('orders:table_order', args=[uuid.uuid4(), uuid.uuid4()])
        assert resolve(path).view_name == 'orders:table_order'

    def test_create_table_order_get(self):
        path = reverse('orders:create_table_order')
        assert resolve(path).view_name == 'orders:create_table_order'

    def test_waiter_checkout(self):
        path = reverse('orders:checkout', args=[uuid.uuid4()])
        assert resolve(path).view_name == 'orders:checkout'

