from rest_framework import serializers

from .models import Activity, User


class UserSerializer(serializers.ModelSerializer):
    activitys = serializers.PrimaryKeyRelatedField(
        queryset=Activity.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = User
        fields = ['id', 'name', 'activitys']


class ActivitySerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Activity
        fields = ['id', 'title', 'description', 'users']
