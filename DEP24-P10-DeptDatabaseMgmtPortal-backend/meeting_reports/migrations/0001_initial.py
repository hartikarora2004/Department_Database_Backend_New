# Generated by Django 3.2.18 on 2023-04-16 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('batch', '0001_initial'),
        ('department', '0018_department_programs_offered'),
        ('achievements', '0008_achievement_users'),
        ('publications', '0009_publication_accepted_date'),
        ('events', '0007_event_users'),
        ('visits', '0007_visit_users'),
        ('project', '0009_project_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='DinfoMeetingFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(blank=True, null=True)),
                ('batches', models.ManyToManyField(related_name='dinfomeetingfile_batches', to='batch.Batch')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dinfomeetingfile_department', to='department.department')),
                ('events', models.ManyToManyField(related_name='dinfomeetingfile_events', to='events.Event')),
                ('faculty_achievements', models.ManyToManyField(related_name='dinfomeetingfile_faculty_achievements', to='achievements.Achievement')),
                ('faculty_visits', models.ManyToManyField(related_name='dinfomeetingfile_faculty_visits', to='visits.Visit')),
                ('projects', models.ManyToManyField(related_name='dinfomeetingfile_projects', to='project.Project')),
                ('publications', models.ManyToManyField(related_name='dinfomeetingfile_publications', to='publications.Publication')),
                ('student_achievements', models.ManyToManyField(related_name='dinfomeetingfile_student_achievements', to='achievements.Achievement')),
                ('student_visits', models.ManyToManyField(related_name='dinfomeetingfile_student_visits', to='visits.Visit')),
            ],
        ),
    ]
