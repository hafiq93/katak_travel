# Generated by Django 4.2 on 2025-01-25 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pack_list_kt', '0016_package_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='date_of_travel',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='info',
            field=models.TextField(blank=True, null=True),
        ),
    ]
