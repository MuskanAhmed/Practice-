from django.urls import path
from .views import PageContentListAPIView,FAQListView

urlpatterns = [
    path('content/', PageContentListAPIView.as_view(), name='page-content-list'),
    path('faqs/', FAQListView.as_view(), name='faq-list'),

]
