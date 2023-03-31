# Generated by Django 4.1.7 on 2023-03-02 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testasset', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('In Use', 'In Use'), ('Vacant', 'Vacant'), ('Disposed', 'Disposed'), ('Missing', 'Missing')], max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('quantity', models.IntegerField(null=True)),
                ('category', models.CharField(choices=[('PC', 'PC'), ('Monitor', 'Monitor'), ('Headset', 'Headset'), ('Laptop', 'Laptop')], max_length=200, null=True)),
                ('description', models.CharField(max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]