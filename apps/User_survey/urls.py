from django.urls import path
from .views import QuestionDetailView, WaitlistEntryAPIView

urlpatterns = [
    path('question/', QuestionDetailView.as_view(), name='question-detail'),
    path('response/', WaitlistEntryAPIView.as_view(), name='waitlist-entry'),
]
