from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if(created):
        Token.objects.create(user = instance)

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

class Questionnaire(models.Model):
    name = models.CharField(max_length=50)
    is_survey = models.BooleanField(default=True) #Survey = True; Questionnaire = False

class Event(models.Model):
    name = models.CharField(max_length=50, name="Event Name", )
    description = models.CharField(max_length=500, name="Description")
    start = models.DateTimeField(name="Start Time")
    end = models.DateTimeField(name="End Time")
    questionnaire = models.ForeignKey(Questionnaire, models.SET_NULL, null=True, related_name="events_q")
    survey = models.ForeignKey(Questionnaire, models.SET_NULL, null=True, related_name="events_s")

class Group(models.Model):
    name = models.CharField(max_length=50)
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE
    )
    evaluator = models.ForeignKey(
        Person,
        on_delete=models.CASCADE
    )
    class Meta:
        unique_together = (("event", "evaluator"),)

class Question(models.Model):
    text = models.CharField(max_length=500, name="text")
    op1 = models.CharField(max_length=250, name="op1")
    op2 = models.CharField(max_length=250, name="op2")
    op3 = models.CharField(max_length=250, name="op3")
    op4 = models.CharField(max_length=250, name="op4")
    op5 = models.CharField(max_length=250, name="op5")
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name="questions")

class QuestionnaireAns(models.Model):
    candidate = models.ForeignKey(Person, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(Person, null=True, on_delete=models.CASCADE, related_name="questionnaireAns_e")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    ans = models.IntegerField(name="answer", validators=[
            MaxValueValidator(4),
            MinValueValidator(0)
        ])
    class Meta:
        unique_together = (("candidate", "question"),)

class Resume(models.Model):
    file = models.FileField()
    def __str__(self):
       return self.file.name

class Job(models.Model):
    name = models.CharField(max_length=50, name="Job Title")
    description = models.CharField(max_length=100000, name="Description")

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
        on_delete=models.SET_NULL,
        related_name="candidates"
    )
    resume = models.ForeignKey(
        Resume,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    class Meta:
        unique_together = (("event", "candidate"),)