from django.conf.urls import url
from django.urls import include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from members.views import UserModelViewSet, ProfileModelViewSet
from posts.views import PostModelViewSet, CommentModelViewSet, PostLikeModelViewSet, CommentLikeModelViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'users', UserModelViewSet)
router.register(r'posts', PostModelViewSet)

users_router = routers.NestedSimpleRouter(router, r'users')
post_like_router = routers.NestedSimpleRouter(router, r'posts')
post_like_router.register('like', PostLikeModelViewSet)
post_like_router.register('comments', CommentModelViewSet)

comment_like_router = routers.NestedSimpleRouter(post_like_router, r'comments')
comment_like_router.register('like', CommentLikeModelViewSet)

users_router.register(r'posts', PostModelViewSet)
users_router.register(r'profile', ProfileModelViewSet)

posts_router = routers.NestedSimpleRouter(users_router, 'posts')
posts_router.register('comments', CommentModelViewSet)

urlpatterns = [
    url('', include(router.urls)),
    url('', include(users_router.urls)),
    url('', include(post_like_router.urls)),
    url(r'', include(posts_router.urls)),
    url(r'', include(comment_like_router.urls)),
]
