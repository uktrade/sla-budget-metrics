# Generated by Django 3.2.5 on 2021-08-03 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='applications',
            name='app_guid',
            field=models.CharField(default=12234, max_length=90),
            preserve_default=False,
        ),
    ]
