from django.db import models
from django.contrib.auth.models import AbstractUser

class Group(models.Model):
    pass

class Person(AbstractUser):
    first_name = models.CharField(max_length=50, name="First Name", default="None")
    last_name = models.CharField(max_length=50, name="Last Name", default="None")
    email = models.EmailField(max_length=254, name="Email Address", default="None")


class Candidate(models.Model):
    person = models.ForeignKey(
        Person, 
        on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL
    )
    phone_number = models.CharField(max_length=10, name='Phone Number')
    date_of_birth = models.DateField(name='Date of Birth')


class Evaluator(models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE
    )

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
        Candidate,
        on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL
    )