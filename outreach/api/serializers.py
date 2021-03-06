from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from api.models import Group, Person, Registered, Event, Questionnaire, Question, QuestionnaireAns, Resume, Job
from django.core.validators import MaxLengthValidator, ProhibitNullCharactersValidator, EmailValidator
from django.contrib.auth import authenticate

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            'id',  
            'email', 
            'first_name', 
            'last_name',
            'password'
        ]
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        person = Person(**validated_data)
        password = self.validated_data['password']
        person.set_password(password)
        person.save()
        return person
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

class CandidateSerializer(PersonSerializer):
    phone_number = serializers.CharField(min_length=10, max_length=10, allow_blank=False)
    class Meta(PersonSerializer.Meta):
        model = Person
        fields = PersonSerializer.Meta.fields + ["phone_number"]

def authCheck(email, password):
    query = Person.objects.filter(email=email)
    if(len(query) == 0):
        return True
    user = authenticate(username = email, password = password)
    if(user):
        return True
    return False

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = "__all__"
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"

class RegistrationSerializer(serializers.ModelSerializer):
    class CandSerializerNoUniqueEmail(CandidateSerializer):
        def validate(self,data):
            chk = authCheck(data['email'], data['password'])
            if(chk):
                return data
            raise serializers.ValidationError("Wrong email or password.")
        class Meta(CandidateSerializer.Meta):
            extra_kwargs = {
                'email' : {'validators' : [MaxLengthValidator, ProhibitNullCharactersValidator, EmailValidator]},
                'password': {
                    'write_only': True
                }
            }

    candidate = CandSerializerNoUniqueEmail()
    class Meta:
        model = Registered
        fields = [
            "id",
            "event",
            "candidate",
            "group",
            "resume"
        ]
    def validate(self, data):
        if(self.context['request'].method == 'PATCH'):
            return super(
            RegistrationSerializer, 
            self).validate(data)
        dupTest = Registered.objects.filter(candidate__email=data['candidate']['email']).filter(event__id=data["event"].id)
        if len(dupTest) > 0:
            raise serializers.ValidationError("You are already registered for this event.")
        return data

    def create(self, validated_data):
        cand_info = validated_data.pop('candidate')
        query = Person.objects.filter(email=cand_info["email"])
        if len(query) == 0:
            candSerializer = CandidateSerializer(data=cand_info)
            candSerializer.is_valid()
            cand = candSerializer.save()
        else:
            cand = query[0]
            CandidateSerializer().update(cand, validated_data=cand_info)
        validated_data["candidate"] = cand
        reg = Registered.objects.create(**validated_data)
        reg.save()
        return reg

class EventSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        if('questionnaire' in attrs and attrs['questionnaire'] is not None and not attrs['questionnaire'].is_survey==False):
            raise serializers.ValidationError("The given questionnaire is a survey.")
        if('survey' in attrs and attrs['survey'] is not None and not attrs['survey'].is_survey==True):
            raise serializers.ValidationError("The given survey is a questionnaire.")
        return attrs
    
    class Meta:
        model = Event
        fields = [
            'id',
            'Event Name',
            'Description',
            'Start Time',
            'End Time',
            'survey',
            'questionnaire'
        ]

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'op1', 'op2', 'op3', 'op4', 'op5', 'questionnaire']


class QuestionnaireSerializer(serializers.ModelSerializer):
    events = serializers.PrimaryKeyRelatedField(read_only=True, many=True, source='events_q')
    questions = QuestionSerializer(many=True, required=False)
    is_survey = serializers.HiddenField(default=False)
    class Meta:
        model = Questionnaire
        fields = ['id', 'name', 'events', 'questions', 'is_survey']
        read_only_fields = ('questions',)

class SurveySerializer(QuestionnaireSerializer):
    events = serializers.PrimaryKeyRelatedField(read_only=True, many=True, source='events_s')
    is_survey = serializers.HiddenField(default=True)


class AnswerSerializer(serializers.ModelSerializer):
    def get_unique_together_validators(self):
        return []
    def create(self, validated_data):
        obj = QuestionnaireAns.objects.filter(candidate=validated_data["candidate"],question=validated_data["question"])
        if(len(obj)==0):
            return super().create(validated_data)
        else:
            return super().update(obj[0], validated_data)
    class Meta:
        model = QuestionnaireAns
        fields = ['id', 'candidate', 'evaluator', 'question', 'answer']

class AnswerListSerializer(AnswerSerializer):
    question = QuestionSerializer()

class GroupSerializer(serializers.ModelSerializer):
    evaluator = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), default=serializers.CurrentUserDefault())
    class Meta:
        model = Group
        fields = ['id', 'name', 'event', 'evaluator', 'candidates']
        extra_kwargs = {
            'candidates': {'read_only': True},
        }
