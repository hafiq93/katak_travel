# Generated by Django 4.2 on 2025-04-07 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_kt', '0023_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='allowed_roles',
            field=models.ManyToManyField(blank=True, to='admin_kt.roles'),
        ),
    ]
