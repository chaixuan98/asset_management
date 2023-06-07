# Generated by Django 4.1.7 on 2023-04-18 03:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testasset', '0036_alter_asset_asset_no_alter_staff_employee_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='asset_no',
            field=models.CharField(blank=True, default=None, max_length=10, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='categories',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='category', to='testasset.categories'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='staff',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='testasset.staff'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='employee_id',
            field=models.CharField(blank=True, default=None, max_length=10, null=True, unique=True),
        ),
    ]
