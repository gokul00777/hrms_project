# Generated by Django 4.2 on 2023-07-25 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr_management_app', '0003_wageregister_sunday_and_holidays'),
    ]

    operations = [
        migrations.AddField(
            model_name='wageregister',
            name='new_days_payable',
            field=models.CharField(default='', max_length=40),
        ),
    ]
