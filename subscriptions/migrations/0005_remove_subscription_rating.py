# Generated by Django 3.1.7 on 2021-04-16 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0004_auto_20210416_0955'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='rating',
        ),
    ]
