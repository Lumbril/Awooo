from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

UserModel = get_user_model()


class UserRegistrationRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=UserModel.objects.all())])
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return UserModel.objects.create_user(email=validated_data['email'], password=validated_data['password'])

    class Meta:
        model = UserModel
        fields = ('email', 'password', )


class UserRegistrationResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()

    class Meta:
        model = UserModel
        fields = ('id', 'email')


class RecoveryRequestCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        model = UserModel
        fields = ('email',)


class RecoverySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.IntegerField()

    class Meta:
        model = UserModel
        fields = ('email', 'code',)
