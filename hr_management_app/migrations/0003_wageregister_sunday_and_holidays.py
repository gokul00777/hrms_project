# Generated by Django 4.2 on 2023-07-25 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr_management_app', '0002_remove_wageregister_sunday_and_holidays'),
    ]

    operations = [
        migrations.AddField(
            model_name='wageregister',
            name='sunday_and_holidays',
            field=models.CharField(default='', max_length=40),
        ),
    ]
