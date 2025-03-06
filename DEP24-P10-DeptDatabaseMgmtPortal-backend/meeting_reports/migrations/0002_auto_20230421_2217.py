# Generated by Django 3.2.18 on 2023-04-21 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('visits', '0009_visit_tags'),
        ('project', '0011_project_tags'),
        ('achievements', '0010_achievement_tags'),
        ('batch', '0001_initial'),
        ('events', '0009_event_tags'),
        ('department', '0018_department_programs_offered'),
        ('publications', '0012_publication_field_tags'),
        ('meeting_reports', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dinfomeetingfile',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='dinfomeetingfile',
            name='batches',
            field=models.ManyToManyField(blank=True, null=True, related_name='dinfomeetingfile_batches', to='batch.Batch'),
        ),
        migrations.AlterField(
            model_name='dinfomeetingfile',
            name='events',
            field=models.ManyToManyField(blank=True, null=True, related_name='dinfomeetingfile_events', to='events.Event'),
        ),
        migrations.AlterField(
            model_name='dinfomeetingfile',
            name='faculty_achievements',
            field=models.ManyToManyField(blank=True, null=True, related_name='dinfomeetingfile_faculty_achievements', to='achievements.Achievement'),
        ),
        migrations.AlterField(
            model_name='dinfomeetingfile',
            name='faculty_visits',
            field=models.ManyToManyField(blank=True, null=True, related_name='dinfomeetingfile_faculty_visits', to='visits.Visit'),
        ),
        migrations.AlterField(
            model_name='dinfomeetingfile',
            name='projects',
            field=models.ManyToManyField(blank=True, null=True, related_name='dinfomeetingfile_projects', to='project.Project'),
        ),
        migrations.AlterField(
            model_name='dinfomeetingfile',
            name='publications',
            field=models.ManyToManyField(blank=True, null=True, related_name='dinfomeetingfile_publications', to='publications.Publication'),
        ),
        migrations.AlterField(
            model_name='dinfomeetingfile',
            name='student_achievements',
            field=models.ManyToManyField(blank=True, null=True, related_name='dinfomeetingfile_student_achievements', to='achievements.Achievement'),
        ),
        migrations.AlterField(
            model_name='dinfomeetingfile',
            name='student_visits',
            field=models.ManyToManyField(blank=True, null=True, related_name='dinfomeetingfile_student_visits', to='visits.Visit'),
        ),
        migrations.CreateModel(
            name='BogMeetingFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bogmeetingfile_department', to='department.department')),
                ('events', models.ManyToManyField(blank=True, null=True, related_name='bogmeetingfile_events', to='events.Event')),
                ('faculty_achievements', models.ManyToManyField(blank=True, null=True, related_name='bogmeetingfile_faculty_achievements', to='achievements.Achievement')),
                ('student_achievements', models.ManyToManyField(blank=True, null=True, related_name='bogmeetingfile_student_achievements', to='achievements.Achievement')),
                ('visits', models.ManyToManyField(blank=True, null=True, related_name='bogmeetingfile_visits', to='visits.Visit')),
            ],
        ),
    ]
