# Generated by Django 4.2 on 2024-11-02 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_kt', '0009_userrole_rolepermission'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='no_siri',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='roles',
            name='no_siri',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
