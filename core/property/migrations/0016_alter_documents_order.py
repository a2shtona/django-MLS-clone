# Generated by Django 4.1.7 on 2023-08-23 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0015_rename_documents_documents_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='order',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]