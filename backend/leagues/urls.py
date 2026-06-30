from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import LeagueViewSet, LeagueTeamViewSet, LeagueTeamViewSet

router = DefaultRouter()
router.register('leagues', LeagueViewSet)
router.register('league-teams', LeagueTeamViewSet)

urlpatterns = router.urls