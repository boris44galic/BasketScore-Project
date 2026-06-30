from rest_framework.routers import DefaultRouter
from .views import CountryViewSet, CityViewSet, HallViewSet, SeasonViewSet

router = DefaultRouter()
router.register('countries', CountryViewSet)
router.register('cities', CityViewSet)
router.register('halls', HallViewSet)
router.register('seasons', SeasonViewSet)

urlpatterns = router.urls
