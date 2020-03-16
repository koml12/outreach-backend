from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from api.serializers import PersonSerializer, CandidateSerializer, RegistrationSerializer
from rest_framework.authtoken.models import Token
from api.models import Person
from django.db import transaction
from rest_framework.authtoken.views import ObtainAuthToken
from drf_yasg.utils import swagger_auto_schema

class GetAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        userType = "Evaluator"
        if(user.is_staff):
            userType = "HR"
        elif(user.phone_number):
            userType = "Candidate"
        return Response({'id':user.pk,'token': token.key, 'user_type':userType})