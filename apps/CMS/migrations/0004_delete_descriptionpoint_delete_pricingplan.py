# Generated by Django 5.2.1 on 2025-05-21 08:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CMS', '0003_alter_pagecontent_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DescriptionPoint',
        ),
        migrations.DeleteModel(
            name='PricingPlan',
        ),
    ]
