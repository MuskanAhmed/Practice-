from django.shortcuts import render

# Create your views here.
import json
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from . serializers import SignupSerializer,UserProfileSerializer,ProfileSerializer,ChangePasswordSerializer,CompanyDashboardSerializer
from apps.Users.models import CustomUser
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import UpdateAPIView
from django.contrib.auth import get_user_model

User = get_user_model()







class SignupAPIView(APIView):
    permission_classes = []
    def post(self, request):
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('confirm_password', None)
        if password == confirm_password: 
            serializer = SignupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            response = status.HTTP_201_CREATED
        else:
            data = ''
            raise ValidationError({'password_mismatch': 'Password fields didn not match.'})
        return Response(data, status=response)
    



class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)
    
class AccountSettingsView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def put(self, request):
        user = request.user
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']

        if 'data' in request.data:
            try:
                parsed = json.loads(request.data['data'])
            except json.JSONDecodeError:
                return Response({"error": "Invalid JSON in 'data'"}, status=400)
            serializer = UserProfileSerializer(user, data=parsed)
            if serializer.is_valid():
                serializer.save()
                user.save()
                return Response(UserProfileSerializer(user).data)
            return Response(serializer.errors, status=400)

        return Response({"error": "Missing JSON 'data'"}, status=400)

class ChangePasswordView(UpdateAPIView):
        serializer_class = ChangePasswordSerializer
        model = User
        permission_classes = (IsAuthenticated,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'message': 'Password updated successfully',
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CompanyDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CompanyDashboardSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = CompanyDashboardSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
