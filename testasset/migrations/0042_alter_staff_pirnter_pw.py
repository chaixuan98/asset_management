# Generated by Django 4.1.7 on 2023-05-11 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testasset', '0041_staff_pirnter_pw'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='pirnter_pw',
            field=models.IntegerField(null=True),
        ),
    ]
