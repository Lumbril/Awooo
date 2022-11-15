from rest_framework import serializers

from api.models import Subscription
from api.serializers import UserInfoSerializer


class SubscriptionSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()

    class Meta:
        model = Subscription
        fields = ['user']


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    subscription = serializers.IntegerField()

    class Meta:
        model = Subscription
        fields = ['subscription']


class MySubscriptionSerializer(serializers.ModelSerializer):
    subscription = UserInfoSerializer()

    class Meta:
        model = Subscription
        fields = ['subscription']
