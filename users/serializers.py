from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenPairSerializer(TokenObtainPairSerializer):

    def validate(self, data):
        print(data)
        try:
            user = User.objects.get(email=data.get("username")) or \
                User.objects.get(username=data.get("username"))
        except User.DoesNotExist:
            raise serializers.ValidationError("No such user exists")

        credentials = {
            "password": data.get("password")
        }

        if user:
            credentials["username"] = user.username

        return super().validate(credentials)


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = super(UserCreateSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
