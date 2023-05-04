import pytest
import uuid
from django.test import Client
from django.urls import reverse

from orders.models import PersonalOrder, PersonDraft


@pytest.mark.django_db
def test_create_personal_order_success(client: Client, table_order):
    path = reverse('orders:create_personal_order', args=[table_order.id])

    initial_personal_order_count = PersonalOrder.objects.filter(table_order=table_order).count()

    response = client.post(path)

    assert response.status_code == 302  # Successful form submission should redirect to the table order page.
    assert PersonalOrder.objects.filter(table_order=table_order).count() == initial_personal_order_count + 1


@pytest.mark.django_db
def test_create_personal_order_correct_person_draft(client: Client, table_order, person_1, person_2, person_3):
    # Creating two personal orders with Person 1 and Person 2.
    PersonalOrder.objects.create(table_order=table_order, person=person_1, total=0)
    PersonalOrder.objects.create(table_order=table_order, person=person_2, total=0)
    PersonDraft.objects.create(title='Person 5')
    PersonDraft.objects.create(title='Person 4')

    path = reverse('orders:create_personal_order', args=[table_order.id])
    response = client.post(path)

    assert response.status_code == 302  # Successful form submission should redirect to the table order page.

    # Check if the newly created personal order has the correct PersonDraft (Person 3).
    latest_personal_order = PersonalOrder.objects.filter(table_order=table_order)\
        .exclude(person=person_1)\
        .exclude(person=person_2).first()
    assert latest_personal_order.person.title == person_3.title

