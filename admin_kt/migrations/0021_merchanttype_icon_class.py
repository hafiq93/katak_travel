# Generated by Django 4.2 on 2025-01-11 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_kt', '0020_merchanttype'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchanttype',
            name='icon_class',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
