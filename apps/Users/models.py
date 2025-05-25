from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from cloudinary.models import CloudinaryField



class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    avatar = CloudinaryField('avatar', blank=True, null=True)  

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}" if self.first_name else self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class AdditionalEmail(models.Model):
    EMAIL_TYPE_CHOICES = [
        ('account', 'Account Email'),
        ('company', 'Company Email'),
    ]
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='additional_emails')
    email = models.EmailField()
    type = models.CharField(max_length=20, choices=EMAIL_TYPE_CHOICES, default='account')  

    def __str__(self):
        return f"{self.email} ({self.type})"
    

