# Generated by Django 3.2.18 on 2024-04-11 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usercustom', '0018_alter_customuser_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='description',
        ),
    ]
