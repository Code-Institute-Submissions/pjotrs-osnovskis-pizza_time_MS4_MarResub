# Generated by Django 4.0.1 on 2022-02-24 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0006_rename_f_name_checkoutorder_full_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkoutorder',
            old_name='full_name',
            new_name='f_name',
        ),
        migrations.AddField(
            model_name='checkoutorder',
            name='l_name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
