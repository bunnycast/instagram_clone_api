from django.conf.urls import url
from django.urls import include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from members.views import UserModelViewSet, ProfileModelViewSet
from posts.views import PostModelViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'users', UserModelViewSet)
router.register(r'profile', ProfileModelViewSet)

users_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
users_router.register(r'posts', PostModelViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'', include(users_router.urls)),
]
