from datetime import timedelta
from django.db import models


# Create your models here.

from cloudinary.models import CloudinaryField
from django.conf import settings
from django.utils import timezone



class PricingPlan(models.Model):
    title = models.CharField(max_length=100)
    icon = CloudinaryField('image', blank=True, null=True) 
    subtitle = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stripe_product_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title


class DescriptionPoint(models.Model):
    plan = models.ForeignKey(PricingPlan, related_name='description_points', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.plan.title} - {self.text}"



class UserPackage(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(PricingPlan, on_delete=models.PROTECT)
    activated_on = models.DateTimeField(default=timezone.now)
    expires_on = models.DateTimeField(default=timezone.now() + timedelta(days=30))
    is_active = models.BooleanField(default=True)
    stripe_subscription_id = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expires_on = self.activated_on + timedelta(days=30)
        super().save(*args, **kwargs)