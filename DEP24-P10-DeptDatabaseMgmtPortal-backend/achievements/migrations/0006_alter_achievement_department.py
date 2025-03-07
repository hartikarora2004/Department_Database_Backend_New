# Generated by Django 3.2.18 on 2023-04-05 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0018_department_programs_offered'),
        ('achievements', '0005_alter_achievement_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='department',
            field=models.ManyToManyField(related_name='achievement_department', to='department.Department'),
        ),
    ]
