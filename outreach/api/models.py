from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.conf import settings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if(created):
        Token.objects.create(user = instance)

class Group(models.Model):
    pass

class Person(AbstractUser):
    #first name, last name, email already in abstractUser
    username = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(('email address'), unique=True)
    first_name = models.CharField(('first name'), max_length=30)
    last_name = models.CharField(('last name'), max_length=30)
    phone_number = models.CharField(max_length=10, default=None, blank=True, null=True)
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'
    def __str__(self):
        return "{}".format(self.email)

class Event(models.Model):
    name = models.CharField(max_length=50, name="Event Name")
    description = models.CharField(max_length=500, name="Description")
    start = models.DateTimeField(name="Start Time")
    end = models.DateTimeField(name="End Time")

class Questionnaire(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE
    )

class Survey(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE
    )

class Registered(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE
    )
    candidate = models.ForeignKey(
        Person,
        on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL
    )
    resume = models.CharField(
        max_length=100,
        null=True
    )
    class Meta:
        unique_together = (("event", "candidate"),)