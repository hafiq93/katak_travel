# Generated by Django 4.2 on 2025-04-09 03:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_kt', '0003_company_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='user',
        ),
    ]
