from rest_framework.routers import SimpleRouter

from members.views import UserModelViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'user', UserModelViewSet)

urlpatterns = router.urls
