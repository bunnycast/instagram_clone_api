from django.contrib.auth import get_user_model, authenticate
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from members.serializers import UserSerializer

User = get_user_model()


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['POST'], detail=False)
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
            data = {
                'message': 'token creates',
                'token': token.key,
            }
            return Response(data, status=status.HTTP_201_CREATED)

        data = {
            'message': 'token gets',
            'token': token.key,
        }
        return Response(data, status=status.HTTP_200_OK)
