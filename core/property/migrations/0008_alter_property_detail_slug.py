# Generated by Django 4.0.6 on 2023-07-22 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0007_alter_filter_save_serach_annual_taxes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property_detail',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]