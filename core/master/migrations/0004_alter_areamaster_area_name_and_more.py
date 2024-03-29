# Generated by Django 4.0.6 on 2023-07-27 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0003_languageexcelfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='areamaster',
            name='area_name',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='areamaster',
            name='prefered_name',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='citymaster',
            name='city_name',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='countrymaster',
            name='country_code',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='countrymaster',
            name='country_name',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='couponandpromo',
            name='account_type',
            field=models.JSONField(max_length=300),
        ),
        migrations.AlterField(
            model_name='couponandpromo',
            name='couponcode',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='couponandpromo',
            name='name',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='homecard',
            name='Card_Title',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='homecard',
            name='Card_body',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='homecardtitle',
            name='Subtitle',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='homecardtitle',
            name='Title',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='petmaster',
            name='Pet_Name',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='statemaster',
            name='state_name',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='subscriptionplans',
            name='Name',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='subscriptionplans',
            name='plan_type',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='subscriptionplanservices',
            name='Name',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='subscriptionplanservices',
            name='discount',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='subscriptionplanservices',
            name='plan_type',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='subscriptionservices',
            name='position',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='subscriptionservices',
            name='service_name',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='zipcodemaster',
            name='Zipcode',
            field=models.CharField(max_length=300),
        ),
    ]
