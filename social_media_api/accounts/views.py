from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from django.contrib.auth import get_user_model
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
    
class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_follow = User.object.get(id = user_id)
            if user_to_follow == request.user:
                return Response({"error": "you cannot follow yourself"}, status=400)
            request.user.following.add(user_to_follow)
            return Response({"succes": "you are now following {user_to_follow.username}."})
        except User.DoesNotExist:
            return Response({"error": "user does not exist"}, status=400)
        

class UnfollowUserView(APIView):
    permission_classes =[IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_unfollow = User.objects.get(id=user_id)
            if user_to_unfollow == request.user:
                return Response({"error": "You cannot unfollow yourself."}, status=400)
            request.user.following.remove(user_to_unfollow)
            return Response({"success": f"You have unfollowed {user_to_unfollow.username}."})
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)