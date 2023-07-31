import datetime
from collections import OrderedDict

from django.db.models import Sum
from rest_framework import serializers

from api.models import Dog, Breed, Walk


class DogSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        data['gender'] = bool(data['gender'])

        return super().to_internal_value(data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['gender'] = int(data['gender'])

        walks_total = Walk.objects.filter(dog_id=data['id'], finish__isnull=False,
                                          date_deleted__isnull=True) \
            .aggregate(time_total=Sum('time'), distance_total=Sum('distance'))
        data['time_total'] = int(walks_total['time_total']) \
            if walks_total['time_total'] else 0
        data['distance_total'] = float(walks_total['distance_total']) \
            if walks_total['distance_total'] else 0

        current_datetime = datetime.datetime.now()
        walks_today = Walk.objects.filter(dog_id=data['id'], finish__isnull=False,
                                          date_deleted__isnull=True,
                                          start__year=current_datetime.year,
                                          start__month=current_datetime.month,
                                          start__day=current_datetime.day) \
            .aggregate(distance_today=Sum('distance'))
        data['distance_today'] = int(walks_today['distance_today']) \
            if walks_today['distance_today'] else 0

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
