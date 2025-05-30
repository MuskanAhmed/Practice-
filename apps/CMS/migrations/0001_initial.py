# Generated by Django 5.2.1 on 2025-05-20 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PageContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(choices=[('signup', 'Sign Up'), ('signin', 'Sign In'), ('about', 'About Us'), ('landing_top', 'Landing Page - Top'), ('landing_middle', 'Landing Page - Middle'), ('cart', 'Cart Section')], max_length=50)),
                ('title', models.CharField(blank=True, max_length=255)),
                ('subtitle', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='section_images/')),
                ('order', models.IntegerField(default=0)),
            ],
        ),
    ]
