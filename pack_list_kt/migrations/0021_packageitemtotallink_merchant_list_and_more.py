# Generated by Django 4.2 on 2025-02-01 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pack_list_kt', '0020_remove_productitemtotal_discount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='packageitemtotallink',
            name='merchant_list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='package_details', to='pack_list_kt.merchantpackage'),
        ),
        migrations.AddField(
            model_name='packageitemtotallink',
            name='product_details',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='package_details', to='pack_list_kt.productdetails'),
        ),
    ]
