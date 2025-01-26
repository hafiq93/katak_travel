# Generated by Django 4.2 on 2025-01-26 01:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pack_list_kt', '0017_package_date_of_travel_package_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('product_description', models.TextField()),
                ('product_image', models.ImageField(upload_to='product_images/')),
                ('package_merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_details', to='pack_list_kt.packagemerchant')),
            ],
        ),
    ]
