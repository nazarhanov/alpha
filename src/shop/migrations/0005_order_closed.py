# Generated by Django 3.2.8 on 2021-12-06 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20211202_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]