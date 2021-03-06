from api.models import Group, Person, Registered, Event, Questionnaire, Question, QuestionnaireAns, Resume, Job
from rest_framework import views, viewsets, status
from django.db.models import Count
from rest_framework.response import Response
from api.serializers import GroupSerializer, AnswerSerializer, QuestionSerializer, QuestionnaireSerializer, SurveySerializer, CandidateSerializer, PersonSerializer, RegistrationSerializer, EventSerializer, ResumeSerializer, JobSerializer, AnswerListSerializer
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.permissions import IsEvaluatorOrAdmin, isOwner_Person, isOwner_Registration, IsAdminUserOrReadOnly
from rest_framework.parsers import FileUploadParser
import api.SMS_Notify as SMS_Service

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registered.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [isOwner_Registration]
    def destroy(self, request, *args, **kwargs):
        return viewsets.ModelViewSet.destroy(self, request, *args, **kwargs)
    
    def get_queryset(self):
        qs = Registered.objects.all()
        if('event' in self.request.query_params.keys()):
            qs = qs.filter(event=self.request.query_params['event'])
        if('candidate' in self.request.query_params.keys()):
            qs = qs.filter(candidate=self.request.query_params['candidate'])
        return qs


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

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    def destroy(self, request, *args, **kwargs):
        return viewsets.ModelViewSet.destroy(self, request, *args, **kwargs)

class QuestionnaireViewSet(viewsets.ModelViewSet):
    queryset = Questionnaire.objects.filter(is_survey=False)
    serializer_class = QuestionnaireSerializer

class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Questionnaire.objects.filter(is_survey=True)
    serializer_class = SurveySerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class QuestionAnswerViewSet(viewsets.ModelViewSet):
    queryset = QuestionnaireAns.objects.all()
    serializer_class = AnswerSerializer
    list_serializer_class = AnswerListSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return self.list_serializer_class
        return super(viewsets.ModelViewSet, self).get_serializer_class()

class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsEvaluatorOrAdmin]
    serializer_class = GroupSerializer
    def get_queryset(self):
        qs = Group.objects.all()
        if('event' in self.request.query_params.keys()):
            qs = qs.filter(event=self.request.query_params['event'])
        if('evaluator' in self.request.query_params.keys()):
            qs = qs.filter(evaluator=self.request.query_params['evaluator'])
        return qs

@api_view(['GET'])
def divideGroups(request, eventID):
    registrationsInEvent = list(Registered.objects.filter(event_id=eventID, group_id__isnull=True))
    evaluatorsInEvent = Group.objects.filter(event=eventID)
    if(evaluatorsInEvent == 0):
        return Response({"Error": "There are no evaluators in this event!"})
    for registration in registrationsInEvent:
        group = evaluatorsInEvent.annotate(num_cand=Count('candidates')).order_by('num_cand')[0]
        registration.group = group
        registration.save()
    return Response({"message":"Done."})

class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    #parser_classes = [FileUploadParser]
    serializer_class = ResumeSerializer
    #need to convert PDF into raw file for parser or use a custom parser
    def post(self, request, *args, **kwargs):
        resume_serializer = ResumeSerializer(data=request.data)

        if resume_serializer.is_valid():
            resume_serializer.save()
            return Response(resume_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(resume_serializer.data, status=status.HTTP_400_BAD_REQUEST)

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    def post(self, request, *args, **kwargs):
        resume_serializer = ResumeSerializer(data=request.data)

        if resume_serializer.is_valid():
            resume_serializer.save()
            return Response(resume_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(resume_serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def SMSNotify(request, candidate):
    queryset = Person.objects.filter(id=candidate, phone_number__isnull=False).filter(is_superuser=False)
    if(not queryset):
        return Response({"Error": "No candidate with that ID!"})
    else:
        try:
            SMS_Service.notifyNumber(queryset[0].first_name, queryset[0].phone_number)
            return Response({})
        except:
            return Response({"Error":"There was a problem sending the text."})