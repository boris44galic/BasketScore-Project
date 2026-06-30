from rest_framework.routers import DefaultRouter
from .views import MatchViewSet, StatusViewSet

router = DefaultRouter()
router.register('status', StatusViewSet)
router.register('matches', MatchViewSet)

urlpatterns = router.urls
