# Generated by Django 4.1.7 on 2023-08-22 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_office', '0012_alter_signed_documnets_custom_info_doc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signed_documnets_custom_info',
            name='doc',
            field=models.FileField(blank=True, null=True, upload_to='uploaded_files/signed_documents/%Y-%m-%d'),
        ),
    ]