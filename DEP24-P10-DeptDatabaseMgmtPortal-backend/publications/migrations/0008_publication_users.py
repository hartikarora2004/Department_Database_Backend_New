# Generated by Django 3.2.18 on 2023-04-05 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0007_alter_publication_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='users',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
