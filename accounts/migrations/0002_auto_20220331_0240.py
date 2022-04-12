# Generated by Django 3.2.12 on 2022-03-30 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdevices',
            old_name='device',
            new_name='device_name',
        ),
        migrations.AddField(
            model_name='userdevices',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userdevices',
            name='coordinates',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='userdevices',
            name='device_status',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userdevices',
            name='device_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userdevices',
            name='state',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
