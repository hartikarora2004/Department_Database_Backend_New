# Generated by Django 3.2.18 on 2023-03-28 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usercustom', '0005_customuser_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='get_otp_email',
            field=models.BooleanField(default=False),
        ),
    ]
