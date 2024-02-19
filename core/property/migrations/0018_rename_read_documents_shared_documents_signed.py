# Generated by Django 4.1.7 on 2023-08-23 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0017_remove_documents_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documents',
            old_name='read',
            new_name='shared',
        ),
        migrations.AddField(
            model_name='documents',
            name='signed',
            field=models.BooleanField(default=False),
        ),
    ]