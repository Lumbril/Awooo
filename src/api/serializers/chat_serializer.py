from rest_framework import serializers

from api.models import NameChat


class NameChatResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = NameChat
        depth = 1
        fields = '__all__'
