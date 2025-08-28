from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model extending Django's AbstractUser"""
    
    # Override username to make it required and unique
    username = models.CharField(max_length=150, unique=True, null=False, blank=False)
    
    # Add custom fields
    is_admin = models.BooleanField(default=False)
    
    # Override created_at and updated_at to use Django's auto_now_add and auto_now
    date_joined = models.DateTimeField(auto_now_add=True)  # This replaces created_at
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username
