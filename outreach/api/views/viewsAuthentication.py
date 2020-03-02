from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from api.serializers import EvaluatorSerializer, PersonSerializer, CandidateSerializer, RegistrationSerializer
from rest_framework.authtoken.models import Token
from api.models import Person
from django.db import transaction

class SignupIntoEvent(APIView):
    def post(self, request, **kwargs):
        request.data["event"] = kwargs["event"]
        person = None
        trans = PersonSerializer(data=request.data)
        try:
            with transaction.atomic():
                if trans.is_valid():
                    trans = trans.save()
                    person = trans
                    request.data["person"] = trans.pk
                    candidate = CandidateSerializer(data=request.data)
                    if candidate.is_valid():
                        trans = candidate.save()
                        request.data["candidate"] = trans.pk
                        reg = RegistrationSerializer(data=request.data)
                        if reg.is_valid():
                            trans = reg.save()
                            return Response({"Response": "Added to event.","Token":Token.objects.get(user=person).key}, status=status.HTTP_201_CREATED)
                        else:
                            raise APIException()
                    else:
                        raise APIException()
                else:
                    raise APIException()
        except APIException:
            if("email" in trans.errors and trans.errors["email"][0] == "user with this email address already exists."):
                person = Person.objects.get(email=request.data["email"]).pk
                request.data["candidate"] = person
                reg = RegistrationSerializer(data=request.data)
                if reg.is_valid():
                    reg = reg.save()
                    return Response({"Response": "Added to event.","Token":Token.objects.get(user=person).key}, status=status.HTTP_201_CREATED)
                else:
                    return Response(reg.errors,status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response(trans.errors,status = status.HTTP_400_BAD_REQUEST)
        

class EvalRegister(APIView):
    def post(self, request):
        person = PersonSerializer(data=request.data)
        if person.is_valid():
            per = person.save()
            evalu = EvaluatorSerializer(data={"person": per.pk})
            evalu.is_valid()
            evalu.save()
            return Response({"Response": "Created account.","Token":Token.objects.get(user=per).key}, status=status.HTTP_201_CREATED)
        else:
            return Response(person.errors,status = status.HTTP_400_BAD_REQUEST)
