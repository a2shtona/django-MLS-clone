# Generated by Django 4.1.7 on 2023-08-23 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_office', '0017_remove_customer_info_origin_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer_info',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='virtual_office.virtualofficeteam'),
        ),
    ]
