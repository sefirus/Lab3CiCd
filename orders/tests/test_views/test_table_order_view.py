import uuid as uuid

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from billing.models import Table
from employees.models import Employee, Position
from orders.models import TableOrder, PersonalOrder, PersonDraft


class TestTableOrderView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test_user', 'email@gmail.com', 'password')
        self.table_order_id = uuid.uuid4()
        self.table = Table.objects.create(number=3, name='Table 3')
        self.position = Position.objects.create(title='Waiter')
        self.waiter = Employee.objects.create(position=self.position)
        self.table_order = TableOrder.objects.create(id=self.table_order_id, table=self.table, waiter=self.waiter)
        self.url = reverse('orders:table_order', args=[self.table_order_id])
        self.person = PersonDraft.objects.create(title='Person 1')

    def test_table_order_GET_empty(self):
        self.client.login(username='test_user', password='password')
        response = self.client.get(self.url)
        total = response.context['total']
        table_order = response.context['table_order']
        table_order_has_non_empty_personal_orders = response.context['table_order_has_non_empty_personal_orders']
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'table_order.html')
        self.assertEquals(total, 0)
        self.assertEquals(table_order.id, self.table_order_id)
        self.assertFalse(table_order_has_non_empty_personal_orders)

    def test_table_order_GET_one_empty_po(self):
        self.client.login(username='test_user', password='password')
        po = PersonalOrder.objects.create(table_order=self.table_order, person=self.person, total=0)
        self.table_order.personal_orders.add(po)
        response = self.client.get(self.url)
        total = response.context['total']
        table_order = response.context['table_order']
        table_order_has_non_empty_personal_orders = response.context['table_order_has_non_empty_personal_orders']
        personal_orders = response.context['personal_orders']
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'table_order.html')
        self.assertEquals(total, 0)
        self.assertEquals(table_order.id, self.table_order_id)
        self.assertFalse(table_order_has_non_empty_personal_orders)
        self.assertEquals(len(personal_orders), 1)