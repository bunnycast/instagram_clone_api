from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import viewsets

from posts.models import Post, Comment, PostLike
from posts.serializers import PostSerializer, CommentSerializer, PostUpdateSerializer, CommentUpdateSerializer, \
    PostLikeSerializer

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
        serializer.save(user=self.request.user,
                        post=Post.objects.get(pk=self.kwargs['nested_2_pk']))


class PostLikeModelViewSet(viewsets.ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, post=Post.objects.get(pk=self.kwargs['nested_2_pk']))
