# Generated by Django 5.2.1 on 2025-05-25 05:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Subscription', '0004_remove_userpackage_stripe_subscription_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpackage',
            name='stripe_subscription_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userpackage',
            name='expires_on',
            field=models.DateTimeField(default=datetime.datetime(2025, 6, 24, 5, 51, 52, 272227, tzinfo=datetime.timezone.utc)),
        ),
    ]
