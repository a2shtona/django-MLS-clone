# Generated by Django 4.1.7 on 2023-08-23 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_office', '0019_customer_info_martial_status_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='signed_documnets_custom_info',
            old_name='customobj',
            new_name='virtualprofile',
        ),
    ]
