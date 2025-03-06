# Generated by Django 3.2.18 on 2024-02-20 21:17

from django.db import migrations, models
import usercustom.models


class Migration(migrations.Migration):

    dependencies = [
        ('usercustom', '0013_alter_customuser_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(default='upload/profile.png', upload_to=usercustom.models.profile_upload_path),
        ),
    ]
