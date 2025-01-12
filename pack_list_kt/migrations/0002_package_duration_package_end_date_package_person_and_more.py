# Generated by Django 4.2 on 2025-01-11 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pack_list_kt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='duration',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='person',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('expired', 'Expired')], default='active', max_length=10),
        ),
    ]