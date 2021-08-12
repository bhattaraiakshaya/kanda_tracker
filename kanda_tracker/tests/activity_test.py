import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Activity
from .factories import ActivityFactory, UserFactory

faker = Factory.create()


class Activity_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        ActivityFactory.create_batch(size=3)

    def test_create_activity(self):
        """
        Ensure we can create a new activity object.
        """
        client = self.api_client
        activity_count = Activity.objects.count()
        activity_dict = factory.build(dict, FACTORY_CLASS=ActivityFactory)
        response = client.post(reverse('activity-list'), activity_dict)
        created_activity_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Activity.objects.count() == activity_count + 1
        activity = Activity.objects.get(pk=created_activity_pk)

        assert activity_dict['title'] == activity.title
        assert activity_dict['description'] == activity.description

    def test_create_activity_with_m2m_relations(self):
        client = self.api_client

        users = UserFactory.create_batch(size=3)
        users_pks = [user.pk for user in users]

        activity_dict = factory.build(dict, FACTORY_CLASS=ActivityFactory, users=users_pks)

        response = client.post(reverse('activity-list'), activity_dict)
        created_activity_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED

        activity = Activity.objects.get(pk=created_activity_pk)
        assert users[0].activitys.first().pk == activity.pk
        assert activity.users.count() == len(users)

    def test_get_one(self):
        client = self.api_client
        activity_pk = Activity.objects.first().pk
        activity_detail_url = reverse('activity-detail', kwargs={'pk': activity_pk})
        response = client.get(activity_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('activity-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Activity.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        activity_qs = Activity.objects.all()
        activity_count = Activity.objects.count()

        for i, activity in enumerate(activity_qs, start=1):
            response = client.delete(reverse('activity-detail', kwargs={'pk': activity.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert activity_count - i == Activity.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        activity_pk = Activity.objects.first().pk
        activity_detail_url = reverse('activity-detail', kwargs={'pk': activity_pk})
        activity_dict = factory.build(dict, FACTORY_CLASS=ActivityFactory)
        response = client.patch(activity_detail_url, data=activity_dict)
        assert response.status_code == status.HTTP_200_OK

        assert activity_dict['title'] == response.data['title']
        assert activity_dict['description'] == response.data['description']

    def test_update_title_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        activity = Activity.objects.first()
        activity_detail_url = reverse('activity-detail', kwargs={'pk': activity.pk})
        activity_title = activity.title
        data = {
            'title': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(activity_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert activity_title == Activity.objects.first().title

    def test_update_description_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        activity = Activity.objects.first()
        activity_detail_url = reverse('activity-detail', kwargs={'pk': activity.pk})
        activity_description = activity.description
        data = {
            'description': faker.pystr(min_chars=1001, max_chars=1001),
        }
        response = client.patch(activity_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert activity_description == Activity.objects.first().description
