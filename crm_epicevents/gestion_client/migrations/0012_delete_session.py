# Generated by Django 5.0 on 2024-01-05 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_client', '0011_alter_session_token'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Session',
        ),
    ]
