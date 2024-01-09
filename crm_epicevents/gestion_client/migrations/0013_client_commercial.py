# Generated by Django 5.0 on 2024-01-08 13:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_client', '0012_delete_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='commercial',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clients', to=settings.AUTH_USER_MODEL),
        ),
    ]
