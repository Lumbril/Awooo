import datetime
from collections import OrderedDict

from django.db.models import Sum
from rest_framework import serializers

from api.models import Dog, Breed, Walk, Coordinate
from packs import get_distance


class DogSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        data['gender'] = bool(data['gender'])

        return super().to_internal_value(data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['gender'] = int(data['gender'])

        walks_time_total = Walk.objects.filter(dog_id=data['id']).aggregate(time_total=Sum('time'))

        data['time_total'] = int(walks_time_total['time_total']) \
            if walks_time_total['time_total'] else 0

        points_all = list(Coordinate.objects.select_related('walk__dog')
                          .filter(walk__dog_id=data['id']))
        distance_total = get_distance(points_all)
        data['distance_total'] = distance_total

        current_datetime = datetime.datetime.now()
        points_today = list(Coordinate.objects.select_related('walk__dog')
                            .filter(walk__dog_id=data['id'], walk__date_created__year=current_datetime.year,
                                    walk__date_created__month=current_datetime.month,
                                    walk__date_created__day=current_datetime.day))
        distance_today = get_distance(points_today)
        data['distance_today'] = distance_today
        data['subscribes_count'] = 0

        return data

    class Meta:
        model = Dog
        fields = '__all__'


class DogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog
        exclude = ['account', 'avatar', 'has_avatar']


class DogUpdateSerializer(serializers.ModelSerializer):

    def get_fields(self):
        new_fields = OrderedDict()

        for name, field in super().get_fields().items():
            field.required = False
            new_fields[name] = field

        return new_fields

    class Meta:
        model = Dog
        exclude = ['account', 'has_avatar']


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = '__all__'


class DogAvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(allow_empty_file=False)

    class Meta:
        model = Dog
        fields = ['avatar']
