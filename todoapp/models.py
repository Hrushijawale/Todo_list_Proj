from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models




class CustomUser(AbstractUser):
    def __str__(self):
        return self.username
    
class UserSignIn(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)

from django.db import models
from django.contrib.auth.models import User
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    age = models.PositiveIntegerField()

    def __str__(self):
        return self.user.username

class TodoTask(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    finish_time = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def is_expired(self):
        return timezone.now() > self.finish_time

    def time_left(self):
        return self.finish_time - timezone.now()







