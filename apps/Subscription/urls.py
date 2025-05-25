from django.urls import path
from .views import PricingPlanListView,CreateSubscriptionSession,StripeSubscriptionWebhook,payment_success,CancelSubscriptionView

urlpatterns = [
    path('pricing-plans/', PricingPlanListView.as_view(), name='pricing-plans'),
    path('subscribe/', CreateSubscriptionSession.as_view()),
    path('stripe/webhook/', StripeSubscriptionWebhook.as_view()),
    path('payment-success/', payment_success),
    path('cancel-subscription/', CancelSubscriptionView.as_view(), name='cancel-subscription'),

]
