import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404


class User(AbstractBaseUser, PermissionsMixin):
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
    USERNAME_FIELD = 'user'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self) -> str:
        return f"{self.email}"
    
    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"
