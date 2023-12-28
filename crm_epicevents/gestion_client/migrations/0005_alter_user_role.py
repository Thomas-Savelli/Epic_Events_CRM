# Generated by Django 5.0 on 2023-12-28 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_client', '0004_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('commercial', 'Commercial'), ('support', 'Support'), ('gestion', 'Gestion')], max_length=20),
        ),
    ]