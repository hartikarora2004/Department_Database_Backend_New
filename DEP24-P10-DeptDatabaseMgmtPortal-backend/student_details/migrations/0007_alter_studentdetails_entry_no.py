# Generated by Django 3.2.18 on 2023-04-23 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_details', '0006_auto_20230402_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentdetails',
            name='entry_no',
            field=models.CharField(default='', max_length=20),
        ),
    ]
