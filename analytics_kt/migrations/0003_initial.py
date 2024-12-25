# Generated by Django 4.2 on 2024-12-25 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('analytics_kt', '0002_delete_websiteanalytics'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebsiteAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_url', models.URLField(max_length=255)),
                ('user_ip', models.GenericIPAddressField()),
                ('browser_info', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('event_type', models.CharField(max_length=100)),
            ],
        ),
    ]
