# Generated by Django 3.2.12 on 2022-03-30 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationchannel',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
