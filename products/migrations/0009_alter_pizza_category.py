# Generated by Django 4.0.1 on 2022-02-04 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_remove_product_category_pizza_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='category',
            field=models.ForeignKey(blank=True, default='1', null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.category'),
        ),
    ]
