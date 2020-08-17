from rest_framework.routers import SimpleRouter

from members.views import UserModelViewSet, RelationModelViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'user', UserModelViewSet)
router.register(r'relation', RelationModelViewSet)


urlpatterns = router.urls
