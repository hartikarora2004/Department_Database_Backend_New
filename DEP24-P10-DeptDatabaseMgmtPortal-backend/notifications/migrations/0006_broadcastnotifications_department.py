# Generated by Django 3.2.18 on 2023-05-11 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0018_department_programs_offered'),
        ('notifications', '0005_alter_broadcastnotifications_notification_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='broadcastnotifications',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='broadcastnotifications_department', to='department.department'),
        ),
    ]
