# Generated by Django 4.2 on 2024-12-30 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('package_kt', '0003_subpackage_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subpackage',
            name='parent',
        ),
        migrations.CreateModel(
            name='SubPackage_2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('subpackage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_packages_2', to='package_kt.package')),
            ],
        ),
    ]