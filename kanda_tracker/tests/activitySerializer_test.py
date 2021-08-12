from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from kanda_tracker.serializers import ActivitySerializer

from .factories import ActivityFactory


class ActivitySerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.activity = ActivityFactory.create()

    def test_that_a_activity_is_correctly_serialized(self):
        activity = self.activity
        serializer = ActivitySerializer
        serialized_activity = serializer(activity).data

        assert serialized_activity['id'] == activity.id
        assert serialized_activity['title'] == activity.title
        assert serialized_activity['description'] == activity.description
