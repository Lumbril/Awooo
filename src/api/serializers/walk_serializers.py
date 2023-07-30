from rest_framework import serializers

from api.models import Walk, Coordinate
from packs import get_distance


class CoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinate
        fields = '__all__'


class WalkSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)

        points = list(Coordinate.objects.filter(walk_id=data['id']))
        distance = get_distance(points)
        data['distance'] = distance

        return data

    class Meta:
        model = Walk
        fields = ['id', 'start', 'finish', 'time']


class WalkDetailSerializer(serializers.ModelSerializer):
    coordinate_set = CoordinateSerializer(many=True, read_only=True)

    class Meta:
        model = Walk
        fields = '__all__'
