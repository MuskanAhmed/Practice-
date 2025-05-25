from rest_framework import serializers
from apps.CMS.models import PageContent,FAQ

class PageContentSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PageContent
        fields = ['id', 'title', 'subtitle', 'description', 'section', 'order', 'image_url']

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']
