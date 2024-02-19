# Generated by Django 4.0.6 on 2023-07-21 12:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import secrets


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0008_alter_card_card_number'),
        ('master', '0003_languageexcelfile'),
        ('property', '0005_remove_invitation_userid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Property_Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('property_title', models.CharField(blank=True, max_length=255, null=True)),
                ('propert_description', models.TextField(blank=True, null=True)),
                ('property_main_image', models.FileField(blank=True, null=True, upload_to='Property_main_image')),
                ('property_main_floor_plan', models.FileField(blank=True, null=True, upload_to='Property_main_floor_plan')),
                ('property_address_1', models.TextField(blank=True, null=True)),
                ('property_address_2', models.TextField(blank=True, null=True)),
                ('property_zip', models.CharField(blank=True, max_length=256, null=True)),
                ('property_terms', models.CharField(blank=True, max_length=100, null=True)),
                ('property_offer', models.CharField(blank=True, max_length=100, null=True)),
                ('is_property_fee', models.BooleanField(blank=True, default=False, null=True)),
                ('fees', models.CharField(blank=True, max_length=10, null=True)),
                ('SellerAgency', models.CharField(blank=True, max_length=10, null=True)),
                ('BuyerAgency', models.CharField(blank=True, max_length=10, null=True)),
                ('property_listing_amount', models.FloatField(blank=True, null=True)),
                ('property_cost_per_sq', models.IntegerField(blank=True, null=True)),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('created_time', models.TimeField(auto_now_add=True, null=True)),
                ('property_pet_friendly', models.BooleanField(blank=True, default=False, null=True)),
                ('min_30_shows', models.BooleanField(blank=True, default=False, null=True)),
                ('open_house', models.BooleanField(blank=True, default=False, null=True)),
                ('No_sure_Pet_allowed', models.BooleanField(blank=True, default=True, null=True)),
                ('Bedrooms', models.IntegerField(blank=True, null=True)),
                ('Bathrooms', models.IntegerField(blank=True, null=True)),
                ('Square_sqft', models.IntegerField(blank=True, null=True)),
                ('Exterior_Sqft', models.IntegerField(blank=True, null=True)),
                ('Maintence_fee', models.IntegerField(blank=True, null=True)),
                ('Real_Estate_Tax', models.IntegerField(blank=True, null=True)),
                ('Financing', models.IntegerField(blank=True, null=True)),
                ('Minimum_Down', models.IntegerField(blank=True, null=True)),
                ('Units', models.IntegerField(blank=True, null=True)),
                ('Rooms', models.IntegerField(blank=True, null=True)),
                ('Block', models.IntegerField(blank=True, null=True)),
                ('Lot', models.IntegerField(blank=True, null=True)),
                ('Zone', models.IntegerField(blank=True, null=True)),
                ('Building_Sqft', models.IntegerField(blank=True, null=True)),
                ('Lot_Dimensions', models.IntegerField(blank=True, null=True)),
                ('Building_Dimension', models.IntegerField(blank=True, null=True)),
                ('Stories', models.IntegerField(blank=True, null=True)),
                ('FAR', models.IntegerField(blank=True, null=True)),
                ('Assessment', models.IntegerField(blank=True, null=True)),
                ('Annual_Taxes', models.IntegerField(blank=True, null=True)),
                ('Available_Air_Rights', models.IntegerField(blank=True, null=True)),
                ('Apt', models.CharField(blank=True, max_length=100, null=True)),
                ('is_property_open', models.BooleanField(default=True)),
                ('is_property_expired', models.BooleanField(default=False)),
                ('is_property_exclusive', models.BooleanField(default=False)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('property_area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='master.areamaster')),
                ('property_city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='master.citymaster')),
                ('property_listing_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='property.propertylisting_type')),
                ('property_main_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='property.property_main_category')),
                ('property_state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='master.statemaster')),
                ('property_sub_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='property.property_sub_category')),
                ('property_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='property.property_type')),
                ('propertylisting_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='property.property_listing_type')),
                ('user_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Terms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usertypeobj', models.IntegerField(blank=True, null=True)),
                ('terms', models.TextField(blank=True, null=True)),
                ('position', models.IntegerField(blank=True, null=True)),
                ('property_listing_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='property.propertylisting_type')),
                ('propertylisting_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='property.property_listing_type')),
            ],
        ),
        migrations.CreateModel(
            name='TeamProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('propertydetail_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='property.property_detail')),
                ('userprofile_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Seen_Property_listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_detail_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.property_detail')),
                ('user_profile_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meet', models.BooleanField(blank=True, null=True)),
                ('Knowledge', models.IntegerField(default=0)),
                ('Professionalism', models.IntegerField(default=0)),
                ('Customer_Service', models.IntegerField(default=0)),
                ('Respectful', models.IntegerField(default=0)),
                ('Recommend', models.IntegerField(default=0)),
                ('experience', models.TextField(blank=True, null=True)),
                ('created_date', models.DateField(blank=True, null=True)),
                ('AgentUser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Property_Space_Availability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('space', models.CharField(blank=True, max_length=256, null=True)),
                ('size', models.CharField(blank=True, max_length=256, null=True)),
                ('term', models.CharField(blank=True, max_length=256, null=True)),
                ('rate', models.CharField(blank=True, max_length=256, null=True)),
                ('type', models.CharField(blank=True, max_length=256, null=True)),
                ('Property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.property_detail')),
            ],
        ),
        migrations.CreateModel(
            name='Property_listing_event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_listing_start_date', models.DateTimeField(blank=True, null=True)),
                ('property_listing_end_date', models.DateTimeField(blank=True, null=True)),
                ('property_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.property_detail')),
            ],
        ),
        migrations.CreateModel(
            name='Property_Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_image_type', models.CharField(blank=True, max_length=255, null=True)),
                ('property_image', models.ImageField(upload_to='property_image')),
                ('is_active', models.BooleanField(default=True)),
                ('property_detail_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.property_detail')),
            ],
        ),
        migrations.CreateModel(
            name='Property_Amenities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amenities_value', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('amenites_master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.amenities_master')),
                ('property_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.property_detail')),
            ],
        ),
        migrations.CreateModel(
            name='Property30minshow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Monday', models.JSONField(blank=True, null=True)),
                ('Tuesday', models.JSONField(blank=True, null=True)),
                ('Wednesday', models.JSONField(blank=True, null=True)),
                ('Thursday', models.JSONField(blank=True, null=True)),
                ('Friday', models.JSONField(blank=True, null=True)),
                ('Saturday', models.JSONField(blank=True, null=True)),
                ('Sunday', models.JSONField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('property_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.property_detail')),
            ],
        ),
        migrations.CreateModel(
            name='PetProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('pet_master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.petmaster')),
                ('property_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.property_detail')),
            ],
        ),
        migrations.CreateModel(
            name='OpenHouseProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Monday', models.JSONField(blank=True, null=True)),
                ('Tuesday', models.JSONField(blank=True, null=True)),
                ('Wednesday', models.JSONField(blank=True, null=True)),
                ('Thursday', models.JSONField(blank=True, null=True)),
                ('Friday', models.JSONField(blank=True, null=True)),
                ('Saturday', models.JSONField(blank=True, null=True)),
                ('Sunday', models.JSONField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('property_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.property_detail')),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usertypeobj', models.IntegerField(blank=True, null=True)),
                ('offer', models.TextField(blank=True, null=True)),
                ('position', models.IntegerField(blank=True, null=True)),
                ('property_listing_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='property.propertylisting_type')),
                ('propertylisting_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='property.property_listing_type')),
            ],
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('token', models.CharField(default=secrets.token_hex, max_length=64)),
                ('expiration_date', models.DateTimeField(blank=True, null=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('license', models.CharField(max_length=255)),
                ('is_accept', models.BooleanField(default=False)),
                ('userid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Guest_Users_Save_Listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_property_available', models.BooleanField(default=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('rating', models.IntegerField(default=0)),
                ('property_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.property_detail')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ContactNow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, null=True)),
                ('property_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='property.property_detail')),
                ('userid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('userprofile_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.userprofile')),
            ],
        ),
    ]
