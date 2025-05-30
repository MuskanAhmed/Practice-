# Generated by Django 5.2.1 on 2025-05-22 03:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_survey', '0003_rename_response_userresponse'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaitlistEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('company', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='userresponse',
            name='person_id',
        ),
        migrations.AddField(
            model_name='userresponse',
            name='waitlist_entry',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='User_survey.waitlistentry'),
            preserve_default=False,
        ),
    ]
