# Generated by Django 4.2.7 on 2025-03-11 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_order_delivary_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
