# Generated by Django 4.1.7 on 2023-05-11 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testasset', '0045_rename_pirnter_pw_staff_printer_pw'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
        ),
    ]
