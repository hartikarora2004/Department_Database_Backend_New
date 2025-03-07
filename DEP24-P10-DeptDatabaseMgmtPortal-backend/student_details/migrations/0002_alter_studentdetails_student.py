# Generated by Django 4.1.5 on 2023-03-14 06:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import student_details.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('student_details', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentdetails',
            name='student',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_student', to=settings.AUTH_USER_MODEL, validators=[student_details.models.validate_student]),
        ),
    ]
