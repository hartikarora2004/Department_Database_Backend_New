# Generated by Django 4.1.5 on 2023-03-12 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0009_remove_department_department_department_unique_code_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='department',
            name='department_code_is_unique',
        ),
        migrations.AddConstraint(
            model_name='department',
            constraint=models.UniqueConstraint(condition=models.Q(('is_deleted', False)), fields=('code', 'is_approved'), name='department_code_is_unique'),
        ),
    ]
