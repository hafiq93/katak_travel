# Generated by Django 4.2 on 2025-01-11 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pack_list_kt', '0007_remove_status_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='color',
            field=models.CharField(default='#FFFFFF', max_length=7),
        ),
    ]
