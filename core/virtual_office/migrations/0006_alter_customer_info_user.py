# Generated by Django 4.0.6 on 2023-07-28 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_office', '0005_signed_documnets_custom_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer_info',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='virtual_office.virtualofficeteam'),
        ),
    ]