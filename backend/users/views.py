from rest_framework import generics, permissions, status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Q
from .models import User, FavouriteTeam
from teams.models import Team
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    ChangePasswordSerializer,
    AdminUserSerializer,
    FavouriteTeamSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {'access': str(refresh.access_token), 'refresh': str(refresh)},
            status=status.HTTP_201_CREATED,
        )


class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data['current_password']):
            return Response(
                {'current_password': ['Wrong password.']},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'detail': 'Password changed successfully.'})


class AdminUserViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = AdminUserSerializer
    http_method_names = ['get', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        qs = User.objects.order_by('-date_joined')
        query = (self.request.query_params.get('q') or '').strip()
        if query:
            qs = qs.filter(
                Q(username__icontains=query) | Q(email__icontains=query)
            )
        return qs


class FavouriteTeamListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        favs = FavouriteTeam.objects.filter(user=request.user).select_related(
            'team', 'team__city'
        )
        serializer = FavouriteTeamSerializer(favs, many=True)
        return Response(serializer.data)


class FavouriteTeamToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, team_id):
        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response({'detail': 'Team not found.'}, status=status.HTTP_404_NOT_FOUND)

        fav, created = FavouriteTeam.objects.get_or_create(user=request.user, team=team)
        if not created:
            fav.delete()
            return Response({'is_favourite': False})
        return Response({'is_favourite': True}, status=status.HTTP_201_CREATED)
