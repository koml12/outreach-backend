from rest_framework import serializers
from api.models import Person, Evaluator, Candidate, Registered

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registered
        fields = [
            "event",
            "candidate",
            "group",
            "resume"
        ]
    
    def create(self, validated_data):
        registered = Registered(**validated_data)
        registered.save()
        return registered

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = [
            'person',
            'Phone Number'
        ]
    
    def create(self, validated_data):
        candidate = Candidate(**validated_data)
        candidate.save()
        return candidate


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            'username', 
            'password', 
            'email', 
            'first_name', 
            'last_name'
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

class EvaluatorSerializer(PersonSerializer):
    class Meta:
        model = Evaluator
        fields = ('person',)

    def create(self, validated_data):
        evaluator = Evaluator(**validated_data)
        evaluator.save()
        return evaluator
