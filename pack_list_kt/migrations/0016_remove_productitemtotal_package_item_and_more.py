# Generated by Django 4.2 on 2025-01-30 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pack_list_kt', '0015_alter_productitemtotal_grand_total_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productitemtotal',
            name='package_item',
        ),
        migrations.AddField(
            model_name='productitemtotal',
            name='package_items',
            field=models.ManyToManyField(blank=True, related_name='product_totals', to='pack_list_kt.packageitem'),
        ),
    ]
