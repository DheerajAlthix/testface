from rest_framework import serializers
from .models import UserProfile, ABHAUser, OTPRequest



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class ABHAUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ABHAUser
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class OTPRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPRequest
        fields = '__all__'
        read_only_fields = ('created_at',)



from rest_framework import serializers
from django.contrib.auth.models import User
from .models import OTPRequest

class OTPRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPRequest
        fields = ['txn_id', 'otp', 'is_verified', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
