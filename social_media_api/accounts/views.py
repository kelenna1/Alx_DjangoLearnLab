from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from .models import CustomUser
# Create your views here.

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.id})
        return Response(serializer.errors, status=400)
    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, _ = Token.objects.get_or_create(user= user)
            return Response({'token': token.key, 'user_id': user.id})
        return Response(serializer.errors, status=400)
    
User = get_user_model

class FollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()  # Ensures CustomUser.objects.all() is present
    permission_classes = [IsAuthenticated]  # Explicitly include permissions.IsAuthenticated

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(self.queryset, id=user_id)

        if user_to_follow in request.user.following.all():
            return Response({"detail": "You are already following this user."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(user_to_follow)
        return Response({"detail": "User followed successfully."}, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()  # Ensures CustomUser.objects.all() is present
    permission_classes = [IsAuthenticated]  # Explicitly include permissions.IsAuthenticated

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(self.queryset, id=user_id)

        if user_to_unfollow not in request.user.following.all():
            return Response({"detail": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(user_to_unfollow)
        return Response({"detail": "User unfollowed successfully."}, status=status.HTTP_200_OK)
