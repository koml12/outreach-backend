from rest_framework import serializers
from api.models import Person, Registered

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

class CandidateSerializer(PersonSerializer):
    phone_number = serializers.CharField(min_length=10, max_length=10, allow_blank=False)
    class Meta(PersonSerializer.Meta):
        model = Person
        fields = PersonSerializer.Meta.fields + ["phone_number"]