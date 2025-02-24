# Generated by Django 4.2 on 2025-01-26 02:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_kt', '0022_mainmerchant_merchantlist_merchantlogin_and_more'),
        ('pack_list_kt', '0009_package_user_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='MerchantPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant', models.CharField(max_length=100)),
                ('street_address', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=20, null=True)),
                ('contact_person', models.CharField(blank=True, max_length=50, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='merchant_packages', to='pack_list_kt.location')),
            ],
        ),
        migrations.CreateModel(
            name='PackageMerchant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('merchant_code', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('merchant_list', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='package_merchants', to='pack_list_kt.merchantpackage')),
                ('merchant_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='package_merchants', to='admin_kt.merchanttype')),
            ],
        ),
        migrations.RemoveField(
            model_name='packageitem',
            name='package',
        ),
        migrations.AddField(
            model_name='package',
            name='code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='date_of_travel',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='info',
            field=models.TextField(blank=True, null=True),
        ),
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
        migrations.AddField(
            model_name='packagemerchant',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='package_merchants', to='pack_list_kt.package'),
        ),
        migrations.AddField(
            model_name='packageitem',
            name='merchant_list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pack_price', to='pack_list_kt.packagemerchant'),
        ),
    ]
