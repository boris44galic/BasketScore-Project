from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, FavouriteTeam
from teams.serializers import TeamSerializer
from teams.models import Team


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password_confirm', 'city')

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'city', 'is_staff', 'date_joined')
        read_only_fields = ('id', 'is_staff', 'date_joined')


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff', 'is_active', 'date_joined')
        read_only_fields = ('id', 'email', 'date_joined')


class FavouriteTeamSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), source='team', write_only=True
    )

    class Meta:
        model = FavouriteTeam
        fields = ('id', 'team', 'team_id', 'created_at')
        read_only_fields = ('id', 'created_at')
