# Generated by Django 4.2 on 2025-01-30 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pack_list_kt', '0016_remove_productitemtotal_package_item_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productitemtotal',
            name='package_items',
        ),
        migrations.AddField(
            model_name='productitemtotal',
            name='package_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_totals', to='pack_list_kt.packageitem'),
        ),
    ]
