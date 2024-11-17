from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    def __str__(self):
        return self.username

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None,):
        return
    def create_superuser(self, email, password=None,):
        return
    
class Meta:
    permissions = [
        ("can_view", "Can view Book"),
        ("can_create", "Can create Book"),
        ("can_edit", "Can edit Book"),
        ("can_delete", "Can delete Book"),
    ]
        