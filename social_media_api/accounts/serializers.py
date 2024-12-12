from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()

class UserRegistrationSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password2e', 'bio', 'profile_picture']
        extra_kwargs = {'password': {'write_only':True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username= validated_data['username'],
            email = validated_data.get['email', ''],
            password = validated_data['password'],
            bio = validated_data.get['bio', ''],
            profile_picture = validated_data.get['profile_picture', None]
        )
        Token.objects.create(user=user)
        return user
    
class USerLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("invalid credentials")