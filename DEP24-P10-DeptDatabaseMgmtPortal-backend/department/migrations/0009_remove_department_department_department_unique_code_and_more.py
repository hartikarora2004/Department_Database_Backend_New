# Generated by Django 4.1.5 on 2023-03-12 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0008_remove_department_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='department',
            name='department_department_unique_code',
        ),
        migrations.AddConstraint(
            model_name='department',
            constraint=models.CheckConstraint(check=models.Q(('is_draft', True), ('is_approved', True), _negated=True), name='draft cannot be approved'),
        ),
        migrations.AddConstraint(
            model_name='department',
            constraint=models.UniqueConstraint(condition=models.Q(('is_approved', False), ('is_deleted', True)), fields=('draft_id', 'is_approved', 'is_deleted'), name='Only on draft can be made for each object'),
        ),
        migrations.AddConstraint(
            model_name='department',
            constraint=models.UniqueConstraint(condition=models.Q(('is_deleted', False)), fields=('code', 'is_draft'), name='department_code_is_unique'),
        ),
    ]
