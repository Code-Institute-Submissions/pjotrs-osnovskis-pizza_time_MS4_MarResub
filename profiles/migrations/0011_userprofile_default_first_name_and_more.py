# Generated by Django 4.0.1 on 2022-03-08 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_remove_userprofile_default_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='default_first_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='default_last_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
