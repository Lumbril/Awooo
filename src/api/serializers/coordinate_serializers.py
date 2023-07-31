from rest_framework import serializers

from api.models import Coordinate


class CoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinate
        fields = '__all__'


class CoordinateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinate
        fields = ['latitude', 'longitude', 'walk']
