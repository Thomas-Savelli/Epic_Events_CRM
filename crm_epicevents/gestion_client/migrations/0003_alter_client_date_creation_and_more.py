# Generated by Django 5.0 on 2023-12-28 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_client', '0002_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='date_derniere_maj',
            field=models.DateField(auto_now=True),
        ),
    ]
