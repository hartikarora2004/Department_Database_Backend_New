# Generated by Django 3.2.18 on 2023-04-20 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_project', '0007_studentproject_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentproject',
            name='title',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
