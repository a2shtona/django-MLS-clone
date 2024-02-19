# Generated by Django 4.1.7 on 2023-08-22 16:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_uploadedfiles_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedfiles',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='uploaded_files/documents/%Y-%m-%d', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])]),
        ),
    ]
