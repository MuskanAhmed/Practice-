from django.shortcuts import render


# Create your views here.
from django.utils import timezone 
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.Subscription.models import PricingPlan,UserPackage 
from apps.Users.models import CustomUser
from .serializers import PricingPlanSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
import json
from django.utils.decorators import method_decorator

User = get_user_model()



class PricingPlanListView(APIView):
    permission_classes = [AllowAny]  

    def get(self, request):
        plans = PricingPlan.objects.all()
        serializer = PricingPlanSerializer(plans, many=True)
        return Response(serializer.data)



stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateSubscriptionSession(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        plan_id = request.data.get("plan_id")
        plan = PricingPlan.objects.get(id=plan_id)

        checkout_session = stripe.checkout.Session.create(
            success_url='http://localhost:8000/api/subscription/payment-success/',
            cancel_url='http://localhost:8000/subscription-cancel/',
            payment_method_types=['card'],
            mode='subscription',
            customer_email=request.user.email,
            line_items=[{
                'price': plan.stripe_price_id,
                'quantity': 1,
            }],
            metadata={
                'user_id': request.user.id,
                'plan_id': plan.id
            }
        )
        return Response({"checkout_url": checkout_session.url})


@method_decorator(csrf_exempt, name='dispatch')
class StripeSubscriptionWebhook(APIView):
    permission_classes = []

    def post(self, request):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except stripe.error.SignatureVerificationError:
            return HttpResponse(status=400)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            user_id = session['metadata']['user_id']
            plan_id = session['metadata']['plan_id']
            subscription_id = session.get('subscription')

            user = CustomUser.objects.get(id=user_id)
            plan = PricingPlan.objects.get(id=plan_id)

            UserPackage.objects.update_or_create(
                user=user,
                defaults={
                    'plan': plan,
                    'stripe_subscription_id': subscription_id,
                    'is_active': True
                }
            )

        elif event['type'] == 'customer.subscription.deleted':
            session = event['data']['object']
            subscription_id = session['id']

            try:
                user_package = UserPackage.objects.get(stripe_subscription_id=subscription_id)
                user_package.is_active = False
                user_package.expires_on = timezone.now()
                user_package.save()
            except UserPackage.DoesNotExist:
                pass 

        return JsonResponse({'status': 'success'})



def payment_success(request):
    return JsonResponse({"message": "Payment successful"})




stripe.api_key = settings.STRIPE_SECRET_KEY

class CancelSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user_package = UserPackage.objects.get(user=request.user)
            subscription_id = user_package.stripe_subscription_id

            stripe.Subscription.delete(subscription_id)

            user_package.is_active = False
            user_package.expires_on = timezone.now()  
            user_package.save()

            return Response({"message": "Subscription cancelled successfully"})
        except UserPackage.DoesNotExist:
            return Response({"error": "No subscription found for this user"}, status=404)
        except stripe.error.InvalidRequestError as e:
            return Response({"error": str(e)}, status=400)
