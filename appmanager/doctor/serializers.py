from rest_framework import serializers
from .models import Lookup, HealthCareProvider, PersonalCare

class LookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lookup
        fields = '__all__'  


class HealthCareProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthCareProvider
        fields = '__all__'


class PersonalCareSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalCare
        fields = "__all__" 