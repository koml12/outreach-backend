from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models import Person, Event, Registered, Group, Questionnaire, Resume, Job

# Register your models here.
admin.site.register(Person, UserAdmin)
admin.site.register(Event)
admin.site.register(Registered)
admin.site.register(Group)
admin.site.register(Questionnaire)
admin.site.register(Resume)
admin.site.register(Job)