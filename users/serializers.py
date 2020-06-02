from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenPairSerializer(TokenObtainPairSerializer):

    def validate(self, data):

        try:
            user = User.objects.filter(username=data.get("username")) or \
                User.objects.filter(email=data.get("username"))
        except User.DoesNotExist:
            raise serializers.ValidationError("No such user exists")

        credentials = {
            "username": "",
            "password": data.get("password")
        }

        if user:
            user = user.first()
            credentials["username"] = user.username

        return super().validate(credentials)


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = super(UserCreateSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
