# Generated by Django 4.2 on 2025-04-15 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pack_list_kt', '0035_packagemainimage_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='packageotherimage',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='packageotherimage',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
