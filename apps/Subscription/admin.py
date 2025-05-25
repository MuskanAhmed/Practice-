from django.contrib import admin

# Register your models here.
from unfold.admin import ModelAdmin
from .models import PricingPlan, DescriptionPoint,UserPackage
import stripe
from django.conf import settings

class DescriptionPointInline(admin.TabularInline):
    model = DescriptionPoint
    extra = 1
    fields = ['text', 'order']
    ordering = ['order']
stripe.api_key = settings.STRIPE_SECRET_KEY

class PricingPlanAdmin(ModelAdmin):
    inlines = [DescriptionPointInline]
    list_display = ['title', 'price']
    def save_model(self, request, obj, form, change):
        if not obj.stripe_product_id:
            product = stripe.Product.create(name=obj.title)
            obj.stripe_product_id = product.id

        if not obj.stripe_price_id:
            price = stripe.Price.create(
                unit_amount=int(obj.price * 100),
                currency='usd',
                recurring={"interval": "month"},
                product=obj.stripe_product_id
            )
            obj.stripe_price_id = price.id

        super().save_model(request, obj, form, change)
    
admin.site.register(PricingPlan, PricingPlanAdmin)
admin.site.register(UserPackage)





