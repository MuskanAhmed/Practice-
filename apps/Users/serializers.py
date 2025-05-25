from apps.Users.models import CustomUser,AdditionalEmail
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()



class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}} 
    def create(self, validated_data): 
        if validate_password(validated_data['password']) == None:
            password = make_password(validated_data['password'])                          
            user = CustomUser.objects.create(
                email=validated_data['email'],
                password=password
            )
        return user


class AdditionalEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalEmail
        fields = ['id', 'email']
        extra_kwargs = {
            'type': {'default': 'account'}  
        }

class ProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    additional_emails = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'full_name',
            'company_name',
            'job_title',
            'email',
            'avatar',
            'additional_emails',
        ]
        read_only_fields = fields

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_avatar(self, obj):
        return obj.avatar.url if obj.avatar else None

    def get_additional_emails(self, obj):
        emails = obj.additional_emails.filter(type='account')
        return [e.email for e in emails]


class UserProfileSerializer(serializers.ModelSerializer):
    additional_emails = AdditionalEmailSerializer(many=True)
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'job_title', 'company_name', 'email', 'avatar', 'additional_emails']

    def update(self, instance, validated_data):
        for attr in ['first_name', 'last_name', 'job_title', 'company_name']:
            if attr in validated_data:
                setattr(instance, attr, validated_data[attr])

        additional_emails_data = validated_data.pop('additional_emails', [])
        instance.additional_emails.filter(type='account').delete()

        for email_obj in additional_emails_data:
            email_obj.pop('type', None)  
            AdditionalEmail.objects.create(
                user=instance,
                type='account',
                **email_obj
            )


        instance.save()
        return instance
    def get_avatar(self, obj):
        return obj.avatar.url if obj.avatar else None
    

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)



class CompanyEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalEmail
        fields = ['email']

class CompanyDashboardSerializer(serializers.ModelSerializer):
    company_emails = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['company_emails']

    def get_company_emails(self, instance):
        emails = instance.additional_emails.filter(type='company')
        return CompanyEmailSerializer(emails, many=True).data

    def update(self, instance, validated_data):
        email_data = self.initial_data.get('company_emails', [])

        for email_obj in email_data:
            email_obj.pop('type', None)
            email_address = email_obj.get('email')

            if not instance.additional_emails.filter(email=email_address, type='company').exists():
                AdditionalEmail.objects.create(
                    user=instance,
                    type='company',
                    **email_obj
                )

        return instance




