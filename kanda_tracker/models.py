from django.db import models


class User(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    activitys = models.ManyToManyField(
        'Activity', related_name='users', db_table='user_activity', blank=True)

    class Meta:
        db_table = "user"


class Activity(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        db_table = "activity"
