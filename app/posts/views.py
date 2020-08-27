from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from posts.models import Post, Comment, PostLike, CommentLike
from posts.serializers import PostSerializer, CommentSerializer, PostUpdateSerializer, CommentUpdateSerializer, \
    PostLikeSerializer, CommentLikeSerializer

User = get_user_model()


class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer(self):
        if self.action == 'partial_update':
            return PostUpdateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = Post.objects.filter(user=User.objects.first())
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class CommentModelViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_serializer(self):
        if self.action == 'partial_update':
            return CommentUpdateSerializer
        else:
            return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            post=Post.objects.get(pk=self.kwargs['nested_2_pk'])
        )


class PostLikeModelViewSet(viewsets.ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, post=Post.objects.get(pk=self.kwargs['nested_2_pk']))

    @action(methods=['POST'], detail=False, url_path='toggle')
    def list_toggle(self, request, **kwargs):
        try:
            like = PostLike.objects.get(user=request.user, post=Post.objects.get(pk=self.kwargs['nested_2_pk']))
            like.delete()
            return Response({'message': 'Post Like Deleted'}, status=status.HTTP_204_NO_CONTENT)
        except PostLike.DoesNotExist:
            data = {
                'post': Post.objects.get(pk=self.kwargs['nested_2_pk']).pk,
                'user': request.user.pk,
            }
            serializer = PostLikeSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentLikeModelViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.id, comment=Comment.objects.get(pk=self.kwargs['nested_1_pk']).pk)

    @action(methods=['POST'], detail=False, url_path='toggle')
    def like_toggle(self, request, **kwargs):
        try:
            like = CommentLike.objects.get(user=request.user,
                                           comment=Comment.objects.get(pk=self.kwargs['nested_2_pk']))
            like.delete()
            return Response({'message': 'Post Like Delete'}, status=status.HTTP_204_NO_CONTENT)
        except CommentLike.DoesNotExist:
            data = {
                'comment': Comment.objects.get(pk=self.kwargs['nested_2_pk']).pk,
                'user': request.user.pk,
            }
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED )