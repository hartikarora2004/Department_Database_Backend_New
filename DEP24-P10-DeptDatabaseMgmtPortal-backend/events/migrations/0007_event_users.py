# Generated by Django 3.2.18 on 2023-04-05 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_alter_event_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='users',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
