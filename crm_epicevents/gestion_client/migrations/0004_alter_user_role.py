# Generated by Django 5.0 on 2023-12-28 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_client', '0003_alter_client_date_creation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('C', 'Commercial'), ('S', 'Support'), ('G', 'Gestion')], max_length=20),
        ),
    ]
