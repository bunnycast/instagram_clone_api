from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import viewsets

from posts.models import Post
from posts.serializers import PostSerializer

User = get_user_model()


class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        qs = Post.objects.filter(user=User.objects.first())
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
