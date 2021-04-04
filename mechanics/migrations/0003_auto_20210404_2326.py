# Generated by Django 3.1.7 on 2021-04-04 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mechanics', '0002_auto_20210404_2305'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brand',
            options={'verbose_name_plural': 'Brands'},
        ),
        migrations.AlterField(
            model_name='mechanic',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True),
        ),
    ]
