# Generated by Django 4.0.6 on 2023-07-22 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0006_property_detail_terms_teamproperty_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filter_save_serach',
            name='Annual_Taxes',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='filter_save_serach',
            name='Assessment',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='filter_save_serach',
            name='Available_Air_Rights',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='filter_save_serach',
            name='Bathrooms',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='filter_save_serach',
            name='Bedrooms',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='filter_save_serach',
            name='Zone',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='filter_save_serach',
            name='block',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='filter_save_serach',
            name='building_diamensions',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='filter_save_serach',
            name='far',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='filter_save_serach',
            name='lot',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='filter_save_serach',
            name='lot_diamensions',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='filter_save_serach',
            name='room',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='filter_save_serach',
            name='stories',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='filter_save_serach',
            name='units',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='property_detail',
            name='Apt',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='property_detail',
            name='BuyerAgency',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='property_detail',
            name='SellerAgency',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='property_detail',
            name='fees',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
