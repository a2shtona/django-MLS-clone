# Generated by Django 4.1.7 on 2023-08-25 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0023_document_share_with'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
