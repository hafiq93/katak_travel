# Generated by Django 4.2 on 2025-04-11 01:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_kt', '0027_roles_can_receive_status_update'),
        ('pack_list_kt', '0031_remove_packagelog_user_role_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pack_categories', to='admin_kt.merchanttype')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pack_categories', to='pack_list_kt.package')),
            ],
            options={
                'unique_together': {('package', 'merchant_type')},
            },
        ),
    ]
