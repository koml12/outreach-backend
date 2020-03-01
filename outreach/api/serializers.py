from rest_framework import serializers
from api.models import Person, Evaluator

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
        person = PersonSerializer(**validated_data)
        if person.is_valid():
            person = person.save()
            evaluator = Evaluator({"person":person.pk})
            evaluator.save()
            return evaluator
        else:
            raise serializers.ValidationError("Something went wrong when creating evaluator.")
