# Generated by Django 4.1.5 on 2023-03-15 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_broadcastnotifications_message_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='broadcastnotifications',
            name='notification',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='usernotifications',
            name='notification',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]
