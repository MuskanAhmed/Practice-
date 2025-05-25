from rest_framework import serializers
from apps.Subscription.models import PricingPlan, DescriptionPoint


class DescriptionPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescriptionPoint
        fields = ['text', 'order']

class PricingPlanSerializer(serializers.ModelSerializer):
    icon_url = serializers.SerializerMethodField()
    description_points = DescriptionPointSerializer(many=True, read_only=True)

    class Meta:
        model = PricingPlan
        fields = ['id', 'title', 'icon_url', 'subtitle', 'price', 'description_points']
    def get_icon_url(self, obj):
        return obj.icon.url if obj.icon else None
