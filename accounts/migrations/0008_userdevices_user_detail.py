# Generated by Django 3.2.12 on 2022-03-31 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_remove_userdevices_user_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdevices',
            name='user_detail',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, related_name='user_detail', to='accounts.user'),
        ),
    ]
