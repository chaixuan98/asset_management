# Generated by Django 4.1.7 on 2023-03-31 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testasset', '0017_staff_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='date_created',
            new_name='date_assigned',
        ),
    ]
