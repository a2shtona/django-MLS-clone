# Generated by Django 4.1.7 on 2023-08-23 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_office', '0015_alter_signed_documnets_custom_info_doc'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer_info',
            name='doc1',
            field=models.FileField(blank=True, null=True, upload_to='cunstomer_doc_1'),
        ),
        migrations.AddField(
            model_name='customer_info',
            name='doc2',
            field=models.FileField(blank=True, null=True, upload_to='cunstomer_doc_2'),
        ),
        migrations.AddField(
            model_name='customer_info',
            name='doc3',
            field=models.FileField(blank=True, null=True, upload_to='cunstomer_doc_3'),
        ),
    ]