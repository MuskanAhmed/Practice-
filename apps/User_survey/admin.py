from django.contrib import admin

# Register your models here.
from unfold.admin import ModelAdmin
from .models import Question, Option, UserResponse,WaitlistEntry

class OptionInline(admin.TabularInline):
    model = Option
    extra = 2

class QuestionAdmin(ModelAdmin):
    list_display = ('text', 'question_type', 'order')
    ordering = ('order',)  
    inlines = [OptionInline]


admin.site.register(Question, QuestionAdmin)


class UserResponseInline(admin.TabularInline):
    model = UserResponse
    extra = 0
    readonly_fields = ['selected_options']


class WaitlistEntryAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'company', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'company')
    inlines = [UserResponseInline]

admin.site.register(WaitlistEntry, WaitlistEntryAdmin)
