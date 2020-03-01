from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models import Person, Candidate, Evaluator, HumanResources

# Register your models here.
admin.site.register(Person, UserAdmin)
admin.site.register(Candidate)
admin.site.register(Evaluator)
admin.site.register(HumanResources)
