import uuid

import pytest
from django.contrib.auth.models import User

from billing.models import Table
from employees.models import Employee, Position
from menu.models import MenuItem, Category
from orders.models import TableOrder, PersonDraft, PersonalOrder, GroupOrder
from django.test import Client


@pytest.fixture(scope='session')
def django_db_setup():
    from fit_restaurant import settings
    settings.DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3', 'ATOMIC_REQUESTS': True}


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


@pytest.fixture(autouse=True)
def person_2(db) -> PersonDraft:
    person2 = PersonDraft.objects.create(title='Person 2')
    return person2


@pytest.fixture(autouse=True)
def person_3(db) -> PersonDraft:
    person3 = PersonDraft.objects.create(title='Person 3')
    return person3


@pytest.fixture(autouse=True)
def category(db) -> Category:
    category = Category.objects.create(name='Category 1')
    return category


@pytest.fixture(autouse=True)
def menu_item_1(db, category) -> MenuItem:
    menu_item = MenuItem.objects.create(name='Item 1', price=10, total_weight_grams=100, total_calories=20,
                                        is_prohibited=False, category=category)
    return menu_item


@pytest.fixture(autouse=True)
def menu_item_2(db, category) -> MenuItem:
    menu_item = MenuItem.objects.create(name='Item 2', price=15, total_weight_grams=100, total_calories=15,
                                        is_prohibited=False, category=category)
    return menu_item


@pytest.fixture(autouse=True)
def menu_item_3(db, category) -> MenuItem:
    menu_item = MenuItem.objects.create(name='Item 3', price=20, total_weight_grams=100, total_calories=25,
                                        is_prohibited=False, category=category)
    return menu_item


@pytest.fixture
def personal_order_1(table_order, person_1) -> PersonalOrder:
    personal_order = PersonalOrder.objects.create(table_order=table_order, person=person_1, total=0)
    return personal_order


@pytest.fixture
def personal_order_2(table_order, person_2) -> PersonalOrder:
    personal_order = PersonalOrder.objects.create(table_order=table_order, person=person_2, total=0)
    return personal_order


@pytest.fixture
def group_order_1(table_order) -> GroupOrder:
    group_order = GroupOrder.objects.create(table_order=table_order)
    return group_order

@pytest.fixture(autouse=True)
def personal_order_3(db, table_order, person_3) -> PersonalOrder:
    personal_order = PersonalOrder.objects.create(table_order=table_order, person=person_3, total=0)
    return personal_order

@pytest.fixture(autouse=True)
def personal_order_4(db, table_order, person_4) -> PersonalOrder:
    personal_order = PersonalOrder.objects.create(table_order=table_order, person=person_4, total=0)
    return personal_order

@pytest.fixture(autouse=True)
def personal_order_5(db, table_order, person_5) -> PersonalOrder:
    personal_order = PersonalOrder.objects.create(table_order=table_order, person=person_5, total=0)
    return personal_order

@pytest.fixture(autouse=True)
def person_3(db) -> PersonDraft:
    person3 = PersonDraft.objects.create(title='Person 3')
    return person3

@pytest.fixture(autouse=True)
def person_4(db) -> PersonDraft:
    person4 = PersonDraft.objects.create(title='Person 4')
    return person4

@pytest.fixture(autouse=True)
def person_5(db) -> PersonDraft:
    person5 = PersonDraft.objects.create(title='Person 5')
    return person5
