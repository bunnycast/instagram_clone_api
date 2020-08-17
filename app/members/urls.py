from rest_framework.routers import SimpleRouter

from members.views import UserModelViewSet, RelationModelViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'users', UserModelViewSet)
# router.register(r'relations', RelationModelViewSet)


urlpatterns = router.urls
