# Generated by Django 4.1.7 on 2023-08-23 06:35

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('property', '0018_rename_read_documents_shared_documents_signed'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Documents',
            new_name='Document',
        ),
    ]