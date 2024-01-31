from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class CustomUser(AbstractUser):
    def __str__(self):
        return self.username
    
class UserSignIn(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)

class UserProfile(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, )  
    phone_number = models.CharField(max_length=15)
    age = models.PositiveIntegerField()

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

class SentEmail(models.Model):
    subject = models.CharField(max_length=255)
    recipient = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject





