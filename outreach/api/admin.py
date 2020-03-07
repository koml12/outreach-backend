from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models import Person, Event, Registered

# Register your models here.
admin.site.register(Person, UserAdmin)
admin.site.register(Event)
admin.site.register(Registered)