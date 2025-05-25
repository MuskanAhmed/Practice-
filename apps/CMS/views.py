from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework import generics
from apps.CMS.models import PageContent,FAQ
from .serializers import PageContentSerializer,FAQSerializer
from rest_framework.permissions import AllowAny
#from rest_framework.permissions import IsAuthenticated


class PageContentListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]  
    serializer_class = PageContentSerializer
    def get_queryset(self):
        section = self.request.query_params.get('section')
        if section:
            return PageContent.objects.filter(section=section).order_by('order')
        return PageContent.objects.all()


class FAQListView(generics.ListAPIView):
    permission_classes = [AllowAny]  
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

