from django.db import models

# Create your models here.

from cloudinary.models import CloudinaryField

class PageContent(models.Model):
    section = models.CharField(max_length=50, choices=[
        ('signup', 'Sign Up'),
        ('signin', 'Sign In'),
        ('about', 'About Us'),
        ('landing_top', 'Landing Page - Top'),
        ('landing_middle', 'Landing Page - Middle'),
        ('cart', 'Cart Section')
    ])
    
    title = models.CharField(max_length=255, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    image = CloudinaryField('image', blank=True, null=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.section} - {self.title}"



class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question
