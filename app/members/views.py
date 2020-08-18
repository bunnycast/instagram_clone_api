from django.contrib.auth import get_user_model, authenticate
from rest_framework import viewsets, status, exceptions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from members.models import Relations
from members.serializers import UserSerializer, RelationSerializers, UserCreateSerializer

User = get_user_model()


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    # serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action in ['makeFollow', 'makeBlock', 'create_delete_Relation']:
            return RelationSerializers
        elif self.action == 'create':
            return UserCreateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(context={'request':self.request})

    @action(methods=['POST'], detail=False)
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user is None:
            raise exceptions.AuthenticationFailed('No Such User')
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

    @action(methods=['DELETE'], detail=False)
    def logout(self, request):
        user = request.user
        if user.auth_token:
            user.auth_token.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def follow(self, request):
        users = User.objects.follow
        serializer = UserSerializer(users, many=True, )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def follower(self, request):
        users = User.objects.follower
        serializer = UserSerializer(users, many=True, )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def block(self, request):
        users = User.objects.block
        serializer = UserSerializer(users, many=True, )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def makeBlock(self, request):
        to_user = User.objects.get(pk=request.quert_params.get('toUser'))
        relation_type = request.quert_params.get('type')
        try:
            relation = Relations.objects.get(from_user=request.user, to_user=to_user)
        except Relations.DoesNotExist:
            data = {
                'from_user': request.user.pk,
                'to_user': to_user.pk,
                'related_type': relation_type
            }
            serializer = self.get_serializer(data=data)
            if serializer.is_valid(raise_exceptions=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
        relation.related_type = 'b'
        relation.save()
        return Response({'message': 'change relation'}, status=status.HTTP_200_OK)

    @action(methods=['DELETE'], detail=False)
    def deleteBlock(self, request):
        to_user = User.objects.get(pk=request.query_params.get('toUser'))
        try:
            relation = Relations.objects.get(from_user=request.user, to_user=to_user)
        except Relations.DoesNotExist:
            return Response({"message": "has not relations"}, status=status.HTTP_400_BAD_REQUEST)
        relation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST', 'DELETE', 'PATCH'], detail=False)
    def create_delete_Relation(self, request):
        """
        :param request: relation type이 f면 팔로우, b 면 블락
        1. 이미 팔로우한 유저가 블락을 걸면 이미 존재하는 릴레이션 지우고, 요청에 맞게 재설정
        """
        to_user = User.objects.get(pk=request.query_params.get('toUser'))
        relation_type = request.query_params.get('type')
        method = request._request.method
        data = {
            'from_user': request.user.pk,
            'to_user': to_user.pk,
            'relation_type': relation_type
        }
        try:
            relation = Relations.objects.get(from_user=request.user, to_user=to_user)
            if method == 'PATCH':
                serializers = self.get_serializer(relation, data=data)
                if serializers.is_valid():
                    serializers.save()
                    return Response(serializers.data, status=status.HTTP_200_OK)
                return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
            elif method == 'DELETE':
                relation.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message':'incorrect request.'}, status=status.HTTP_400_BAD_REQUEST)
        except Relations.DoesNotExist:
            if method == 'POST':
                serializer = self.get_serializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

