# Generated by Django 4.1.5 on 2023-03-11 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0005_department_is_approved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='is_approved',
        ),
    ]
