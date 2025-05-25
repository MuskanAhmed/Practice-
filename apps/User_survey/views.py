from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Question, Option, UserResponse,WaitlistEntry
from .serializers import QuestionSerializer,WaitlistEntrySerializer
from rest_framework.permissions import AllowAny
from rest_framework import viewsets


#class QuestionDetailView(APIView):
 #   def get(self, request, pk):  
   ##     try:
    #        question = Question.objects.get(id=pk)
     #   except Question.DoesNotExist:
    #        return Response({"detail": "Question not found"}, status=404)

     #   serializer = QuestionSerializer(question)
      #  return Response(serializer.data)

class QuestionDetailView(APIView):
    permission_classes = [AllowAny]  
    def get(self, request):
        questions = Question.objects.all().order_by('order')  
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

class WaitlistEntryAPIView(APIView):
    permission_classes = [AllowAny]  
    def post(self, request):
        serializer = WaitlistEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
