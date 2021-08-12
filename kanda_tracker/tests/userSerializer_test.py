from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from kanda_tracker.serializers import UserSerializer

from .factories import UserFactory


class UserSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory.create()

    def test_that_a_user_is_correctly_serialized(self):
        user = self.user
        serializer = UserSerializer
        serialized_user = serializer(user).data

        assert serialized_user['id'] == user.id
        assert serialized_user['name'] == user.name
