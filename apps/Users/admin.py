from django.contrib import admin

# Register your models here.
from unfold.admin import ModelAdmin
from .models import CustomUser



@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    model = CustomUser
    list_display = ('email', 'is_active', 'is_staff', 'date_joined')
    ordering = ('email',)
    search_fields = ('email',)

