from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from api.serializers import PersonSerializer, CandidateSerializer, RegistrationSerializer
from rest_framework.authtoken.models import Token
from api.models import Person
from django.db import transaction
from rest_framework.authtoken.views import ObtainAuthToken

class GetAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'id':user.pk,'token': token.key})