# Generated by Django 4.1.7 on 2023-05-11 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testasset', '0042_alter_staff_pirnter_pw'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='pirnter_pw',
            field=models.IntegerField(max_length=7, null=True),
        ),
    ]
