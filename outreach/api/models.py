from django.db import models
from django.contrib.auth.models import AbstractUser

class Person(AbstractUser):
    pass


class Candidate(models.Model):
    person = models.ForeignKey(
        Person, 
        on_delete=models.CASCADE
    )
    phone_number = models.CharField(max_length=10, name='Phone Number')
    date_of_birth = models.DateField(name='Date of Birth')


class Evaluator(models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE
    )


class HumanResources(models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE
    )