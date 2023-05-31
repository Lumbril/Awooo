from rest_framework import serializers


class Http401Serializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField()
    messages = serializers.DictField()
