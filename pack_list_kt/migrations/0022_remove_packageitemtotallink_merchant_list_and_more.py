# Generated by Django 4.2 on 2025-03-23 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pack_list_kt', '0021_packageitemtotallink_merchant_list_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='packageitemtotallink',
            name='merchant_list',
        ),
        migrations.RemoveField(
            model_name='packageitemtotallink',
            name='product_details',
        ),
    ]
