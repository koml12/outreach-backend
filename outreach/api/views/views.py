from api.models import Person, Registered
from rest_framework import views, viewsets, status
from rest_framework.response import Response
from api.serializers import CandidateSerializer, PersonSerializer, RegistrationSerializer
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from api.permissions import isOwner_Person, isOwner_Registration

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registered.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [isOwner_Registration]
    def destroy(self, request, *args, **kwargs):
        return viewsets.ModelViewSet.destroy(self, request, *args, **kwargs)


class EvaluatorViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.filter(phone_number__isnull=True).filter(is_superuser=False)
    serializer_class = PersonSerializer
    permission_classes = [isOwner_Person]
    def destroy(self, request, *args, **kwargs):
        return viewsets.ModelViewSet.destroy(self, request, *args, **kwargs)


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.filter(phone_number__isnull=False).filter(is_superuser=False)
    permission_classes = [isOwner_Person]
    def destroy(self, request, *args, **kwargs):
        return viewsets.ModelViewSet.destroy(self, request, *args, **kwargs)
    def get_serializer_class(self):
        if self.action == 'list':
            return PersonSerializer
        else:
            return CandidateSerializer