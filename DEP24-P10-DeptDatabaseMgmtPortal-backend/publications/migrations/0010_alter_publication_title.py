# Generated by Django 3.2.18 on 2023-04-20 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0009_publication_accepted_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='title',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
