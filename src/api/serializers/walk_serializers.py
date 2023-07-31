from rest_framework import serializers

from api.models import Walk, Coordinate


class CoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinate
        fields = '__all__'


class WalkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Walk
        exclude = ['dog']


class WalkDetailSerializer(serializers.ModelSerializer):
    coordinate_set = CoordinateSerializer(many=True, read_only=True)

    class Meta:
        model = Walk
        fields = '__all__'


class WalkCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Walk.objects.create(**validated_data)

    class Meta:
        model = Walk
        fields = ['start', 'dog']


class WalkPartialUpdateSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        for field in validated_data:
            setattr(instance, field, validated_data.get(field))

        instance.save()

        return instance

    class Meta:
        model = Walk
        fields = ['start', 'finish', 'distance', 'time']
