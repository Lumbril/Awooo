from collections import OrderedDict

from rest_framework import serializers

from api.models import Dog, Breed


class DogSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        data['gender'] = bool(data['gender'])

        return super().to_internal_value(data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['gender'] = int(data['gender'])

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
