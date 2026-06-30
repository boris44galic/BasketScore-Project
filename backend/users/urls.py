from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, LoginView, LogoutView, MeView, ChangePasswordView,
    AdminUserViewSet, FavouriteTeamListView, FavouriteTeamToggleView,
)

router = DefaultRouter()
router.register(r'users/admin', AdminUserViewSet, basename='admin-users')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/me/', MeView.as_view(), name='me'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('favourites/', FavouriteTeamListView.as_view(), name='favourites'),
    path('favourites/<int:team_id>/toggle/', FavouriteTeamToggleView.as_view(), name='favourite-toggle'),
    path('', include(router.urls)),
]
