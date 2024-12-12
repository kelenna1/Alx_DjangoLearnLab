from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):  # Inherit from ModelSerializer
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'bio', 'profile_picture']  # Fixed "password"
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Use create_user to create a new user
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],  # Fixed parenthesis for get
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None)
        )
        # Create a token for the user
        Token.objects.create(user=user)
        return user


class UserLoginSerializer(serializers.Serializer):  # Fixed typo in class name
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # Authenticate the user
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")
