from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


class Testing(APIView):

    permission_classes = (AllowAny, )

    def get(self, request):
        return Response(
            data="API is working fine",
            status=200
        )
