from rest_framework import serializers
from . models import CustomUser
from django.contrib.auth import authenticate

class UserRegistrationSerializer(serializers.Serializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'password2e', 'bio', 'profile_picture']
        extra_kwargs = {'password': {'write_only':True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username= validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password'],
            bio = validated_data.get['bio', ''],
            profile_picture = validated_data.get['profile_picture', None]
        )
        return user
    
class USerLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)

    def validate(self, attrs):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("invalid credentials")