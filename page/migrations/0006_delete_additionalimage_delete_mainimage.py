# Generated by Django 4.2 on 2024-12-02 02:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0005_additionalimage'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AdditionalImage',
        ),
        migrations.DeleteModel(
            name='MainImage',
        ),
    ]
