# Generated by Django 4.2 on 2025-01-01 00:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('package_kt', '0005_alter_subpackage_2_subpackage'),
        ('admin_kt', '0015_delete_websiteanalytics'),
    ]

    operations = [
        migrations.CreateModel(
            name='RolePackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='package_roles', to='package_kt.package')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='role_packages', to='admin_kt.roles')),
            ],
        ),
        migrations.DeleteModel(
            name='RolePermission',
        ),
    ]
