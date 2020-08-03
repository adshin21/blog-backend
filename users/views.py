from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import (
    UserCreateSerializer,
    SocialUserCreateSerializer
)
import requests
from string import ascii_lowercase
from random import randint
from rest_framework_simplejwt.tokens import RefreshToken

from django.conf import settings


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny, )


class SocialLoginView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        provider, code = request.data['provider'], request.data['code']
        if provider == 'github':
            github_response = requests.post(
                "https://github.com/login/oauth/access_token", {
                    "client_id": settings.GITHUB_CLIENT_ID,
                    "client_secret": settings.GITHUB_CLIENT_SECRET,
                    "code": code,
                })

            if github_response.status_code != 200:
                return Response(
                    data="Log in failed",
                    status=400
                )

            access_token = github_response.text.split('&')[0].split('=')[1]

            user_data = requests.get('https://api.github.com/user', headers={
                "Authorization": "token " + access_token
            })

            if user_data.status_code == 200:
                data = user_data.json()
                username, email = data['login'], data['email']

                if email is None:
                    user_emails = requests.get(
                        'https://api.github.com/user/emails',
                        headers={
                            "Authorization": "token " + access_token
                        })

                    for each in user_emails.json():
                        if each['email'] and each['primary'] is True:
                            email = each['email']
                            break

                try:
                    check_user = User.objects.get(email=email)
                except User.DoesNotExist:

                    while True:
                        check_username = User.objects.filter(username=username).exists()
                        if not check_username:
                            break

                        temp_username = ''
                        for i in range(randint(5, 8)):
                            temp_username = ascii_lowercase[randint(0, 25)]
                        temp_username += str(randint(0, 1000))
                        username = temp_username

                    serializer = SocialUserCreateSerializer(data={
                        "email": email,
                        "username": username,
                        "provider": "github"
                    })

                    if serializer.is_valid():
                        user = serializer.save()
                        refresh = RefreshToken.for_user(user)
                        return Response(
                            data={
                                'refresh': str(refresh),
                                'access': str(refresh.access_token)
                            }
                        )

                    else:
                        return Response(
                            data=serializer.errors,
                            status=400
                        )

                if check_user:
                    if provider != "github":
                        return Response(
                            data="Account already exists",
                            status=400
                        )
                    else:
                        refresh = RefreshToken.for_user(check_user)
                        return Response(
                            data={
                                'refresh': str(refresh),
                                'access': str(refresh.access_token)
                            }
                        )
            else:
                return Response(
                    data="Please try later",
                    status=400
                )
        else:
            return Response(
                data="Adding more soon",
                status=400
            )
