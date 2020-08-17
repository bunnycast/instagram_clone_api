from rest_framework.routers import SimpleRouter

from members.views import UserModelViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'users', UserModelViewSet)
# router.register(r'relations', RelationModelViewSet)


urlpatterns = router.urls
