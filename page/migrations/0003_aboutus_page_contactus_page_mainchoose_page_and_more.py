# Generated by Django 4.2 on 2024-11-15 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0002_aboutus_contactus_mainchoose_mainpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutus',
            name='page',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='contactus',
            name='page',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='mainchoose',
            name='page',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='mainpage',
            name='page',
            field=models.TextField(null=True),
        ),
    ]
