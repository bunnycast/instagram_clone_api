from django.shortcuts import render
from rest_framework import viewsets

from posts.models import Post
from posts.serializers import PostSerializer


class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
