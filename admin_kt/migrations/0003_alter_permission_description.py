# Generated by Django 4.2 on 2024-10-28 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_kt', '0002_permission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
    ]
