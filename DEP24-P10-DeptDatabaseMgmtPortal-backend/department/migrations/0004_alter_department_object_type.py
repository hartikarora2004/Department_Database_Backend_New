# Generated by Django 4.1.5 on 2023-03-11 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0003_alter_department_hod_alter_department_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='object_type',
            field=models.CharField(choices=[('A', 'Active'), ('DR', 'Draft'), ('N', 'New')], default='A', max_length=2),
        ),
    ]
