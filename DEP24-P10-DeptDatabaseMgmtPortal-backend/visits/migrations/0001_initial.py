# Generated by Django 4.1.5 on 2023-03-15 17:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_draft', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('draft_id', models.IntegerField(blank=True, null=True)),
                ('object_type', models.CharField(choices=[('DR', 'Draft'), ('P', 'Pending'), ('A', 'Active'), ('R', 'Rejected')], default='A', max_length=2)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('from_date', models.DateField(blank=True, null=True)),
                ('to_date', models.DateField(blank=True, null=True)),
                ('venue', models.TextField(blank=True, null=True)),
                ('type', models.CharField(choices=[('LC', 'Lecture'), ('CF', 'Conference'), ('SM', 'Seminar'), ('O', 'Other')], default='LC', max_length=2)),
                ('description', models.TextField(blank=True, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_authors', to=settings.AUTH_USER_MODEL)),
            ],
            managers=[
                ('allobjects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddConstraint(
            model_name='visit',
            constraint=models.CheckConstraint(check=models.Q(('is_draft', True), ('is_approved', True), _negated=True), name='Visit draft cannot be approved'),
        ),
        migrations.AddConstraint(
            model_name='visit',
            constraint=models.UniqueConstraint(condition=models.Q(('is_approved', False), ('is_deleted', False)), fields=('draft_id', 'is_approved', 'is_deleted'), name='Only one Visit draft can be made for each object'),
        ),
    ]
