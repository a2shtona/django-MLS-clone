# Generated by Django 4.1.7 on 2023-08-23 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0020_remove_document_shared_remove_document_signed'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='shared',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='document',
            name='signed',
            field=models.BooleanField(default=False),
        ),
    ]