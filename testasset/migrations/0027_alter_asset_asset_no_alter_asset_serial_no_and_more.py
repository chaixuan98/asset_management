# Generated by Django 4.1.7 on 2023-04-06 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testasset', '0020_alter_asset_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='asset_no',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='asset',
            name='serial_no',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='staff',
            name='employee_id',
            field=models.CharField(max_length=10),
        ),
    ]
