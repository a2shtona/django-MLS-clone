# Generated by Django 4.1.7 on 2023-08-23 02:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0014_alter_documents_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documents',
            old_name='documents',
            new_name='document',
        ),
    ]