# Generated by Django 3.1.7 on 2021-04-09 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user_credits',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='car_fix_basic',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='car_fix_pro',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='total_credits',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
