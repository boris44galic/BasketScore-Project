from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

from core.models import City


class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None, **extra_fields):

        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            username=username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(
            email,
            username,
            password,
            **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=150, unique=True)

    email = models.EmailField(unique=True)

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class FavouriteTeam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourite_teams')
    team = models.ForeignKey('teams.Team', on_delete=models.CASCADE, related_name='favourited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'team')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} → {self.team.name}'