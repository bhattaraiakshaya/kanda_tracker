from random import randint, uniform

import factory
from factory import LazyAttribute, LazyFunction, SubFactory, fuzzy
from factory.django import DjangoModelFactory
from faker import Factory

from kanda_tracker.models import Activity, User

faker = Factory.create()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    name = LazyAttribute(lambda o: faker.text(max_nb_chars=255))


class ActivityFactory(DjangoModelFactory):
    class Meta:
        model = Activity

    title = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    description = LazyAttribute(lambda o: faker.text(max_nb_chars=1000))
