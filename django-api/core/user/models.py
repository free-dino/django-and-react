import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from core.abstract.models import AbstractManager, AbstractModel
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404


class UserManager(BaseUserManager, AbstractManager):
    def create_user(self, username, email, password=None, **kwargs):
        """Create and return a 'User' with a username, email and password."""
        if username is None:
            raise TypeError("User must have a username")
        if email is None:
            raise TypeError("User must have an email")
        if password is None:
            raise TypeError("User must have a password")

        user = self.model(
            username=username, email=self.normalize_email(email), **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password, **kwargs):
        """Create and return an "User" with superuser (admin) permission"""
        if password is None:
            raise TypeError("Superusers must have a password")
        if email is None:
            raise TypeError("Superusers must have an email")
        if username is None:
            raise TypeError("Superusers must have a username")

        user = self.create_superuser(username, email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractModel, AbstractBaseUser, PermissionsMixin):
    public_id = models.UUIDField(
        db_index=True, unique=True, default=uuid.uuid4, editable=False
    )
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    # when log in, you will have to use email instead of username
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.email}"

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"
