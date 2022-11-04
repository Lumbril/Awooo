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
