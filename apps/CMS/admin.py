from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import PageContent,FAQ


@admin.register(PageContent)
class PageContentAdmin(ModelAdmin):
    list_display = ('section', 'title', 'order')
    list_filter = ('section',)
    ordering = ('section', 'order')
 

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order']
    ordering = ['order']