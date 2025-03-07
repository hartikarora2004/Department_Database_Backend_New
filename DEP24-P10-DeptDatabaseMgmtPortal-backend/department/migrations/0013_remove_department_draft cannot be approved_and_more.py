# Generated by Django 4.1.5 on 2023-03-13 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0012_remove_department_only on draft can be made for each object_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='department',
            name='draft cannot be approved',
        ),
        migrations.RemoveConstraint(
            model_name='department',
            name='Only one draft can be made for each object',
        ),
        migrations.AddConstraint(
            model_name='department',
            constraint=models.CheckConstraint(check=models.Q(('is_draft', True), ('is_approved', True), _negated=True), name='department draft cannot be approved'),
        ),
        migrations.AddConstraint(
            model_name='department',
            constraint=models.UniqueConstraint(condition=models.Q(('is_approved', False), ('is_deleted', False)), fields=('draft_id', 'is_approved', 'is_deleted'), name='department Only one draft can be made for each object'),
        ),
    ]
