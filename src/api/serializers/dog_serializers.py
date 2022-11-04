from collections import OrderedDict

from rest_framework import serializers

from api.models import Dog


class DogSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        instance = super().to_representation(instance)

        if instance['hide_phone']:
            instance.pop('phone')

        return instance

    class Meta:
        model = Dog
        fields = '__all__'


class DogCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dog
        exclude = ['account', 'has_avatar']


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
