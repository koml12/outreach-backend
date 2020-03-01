from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from api.serializers import EvaluatorSerializer, PersonSerializer
from rest_framework.authtoken.models import Token


class SignupIntoEvent(APIView):
    def post(self, request):
        pass

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
            