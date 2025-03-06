# Generated by Django 3.2.18 on 2023-04-22 03:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='QueryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_category', models.CharField(choices=[('Publications', 'Publications'), ('Achievements', 'Achievements'), ('Events', 'Events'), ('Visits', 'Visits'), ('Projects', 'Projects'), ('StudentProjects', 'Studentprojects'), ('BogReports', 'Bogreports'), ('DinfoReports', 'Dinforeports'), ('Other', 'Other')], default='Other', max_length=20)),
                ('issue', models.TextField()),
                ('issue_status', models.CharField(choices=[('Pending', 'Pending'), ('InProgress', 'Inprogress'), ('Resolved', 'Resolved'), ('Rejected', 'Rejected')], default='Pending', max_length=20)),
                ('issue_date', models.DateTimeField(auto_now_add=True)),
                ('issue_resolved', models.TextField(blank=True, null=True)),
                ('screenshot', models.ImageField(blank=True, null=True, upload_to='uploads/% Y/% m/% d/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
