import uuid

import pytest
from django.contrib.auth.models import User

from billing.models import Table
from employees.models import Employee, Position
from orders.models import TableOrder, PersonDraft
from django.test import Client


@pytest.fixture(autouse=True)
def client(test_user):
    user = test_user
    client = Client()
    client.login(username='test_user', password='password')
    return client


@pytest.fixture(autouse=True)
def table_order(db, table_3, employee) -> TableOrder:
    table_order = TableOrder.objects.create(id=uuid.uuid4(), table=table_3, waiter=employee)
    return table_order


@pytest.fixture(autouse=True)
def test_user(db) -> User:
    test_user = User.objects.create_user('test_user', 'email@gmail.com', 'password')
    return test_user


@pytest.fixture(autouse=True)
def table_3(db) -> Table:
    table = Table.objects.create(number=3, name='Table 3')
    return table


@pytest.fixture(autouse=True)
def employee(db) -> Employee:
    position = Position.objects.create(title='Waiter')
    waiter = Employee.objects.create(position=position)
    return waiter


@pytest.fixture(autouse=True)
def person_1(db) -> PersonDraft:
    person1 = PersonDraft.objects.create(title='Person 1')
    return person1

@pytest.fixture(scope='session')
def django_db_setup():
    from fit_restaurant import settings
    settings.DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3', 'ATOMIC_REQUESTS': True}