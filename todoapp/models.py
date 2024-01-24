from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# from todoapp.views import User
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class CustomUser(AbstractUser):
    def __str__(self):
        return self.username
    
class UserSignIn(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)


from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    age = models.IntegerField()
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email_host_user = models.EmailField()
    email_host_password = models.CharField(max_length=255, default='12345')

    def __str__(self):
        return self.user.username


    def __str__(self):
        return self.name

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






