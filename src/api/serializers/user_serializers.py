from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

UserModel = get_user_model()


class UserRegistrationRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=UserModel.objects.all()),
                                               EmailValidator])
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


class ConfirmCodeRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[EmailValidator])
    code = serializers.CharField()


class RecoveryRequestCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[EmailValidator])


class RecoveryCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[EmailValidator])
    code = serializers.CharField()


class RecoverySerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[EmailValidator])
    password = serializers.CharField(write_only=True)
    code = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ['id', 'email']
