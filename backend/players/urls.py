from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet, PlayerStatsViewSet, PlayerMatchStatusViewSet, PositionViewSet

router = DefaultRouter()
router.register('positions', PositionViewSet)
router.register('players', PlayerViewSet)
router.register('player-stats', PlayerStatsViewSet)
router.register('player-match-status', PlayerMatchStatusViewSet)

urlpatterns = router.urls
