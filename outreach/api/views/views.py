from api.models import Person
from rest_framework import views, viewsets
from rest_framework.response import Response
from api.serializers import CandidateSerializer
"""
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
"""

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.filter(phone_number__isnull=False)
    serializer_class = CandidateSerializer
