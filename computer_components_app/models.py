from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone


class Component(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey("Type",on_delete=models.CASCADE)
    manufacturer = models.ForeignKey("Manufacturer",on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def  get_absolute_url(self):
        return reverse('component',kwargs={'pk':self.pk})

class Type(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def  get_absolute_url(self):
        return reverse('type',kwargs={'pk':self.pk})

class Manufacturer(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    def  get_absolute_url(self):
        return reverse('manufacturer',kwargs={'pk':self.pk})
    

class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, unique=True)
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField(null=True, blank=True)
    is_manager = models.BooleanField(default=False)

    def session_duration(self):
        if self.logout_time:
            return self.logout_time - self.login_time
        return timezone.now() - self.login_time

    def __str__(self):
        return f"Session of {self.user.username} started at {self.login_time}"