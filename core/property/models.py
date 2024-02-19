from django.db import models
from accounts.models import *
from master.models import *
from django.utils.text import slugify
import string
from django.db.models.signals import pre_save
from .util import unique_slug_generator
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxLengthValidator, MinLengthValidator
# from accounts.models import UserProfile

class Propertylisting_type(models.Model): #ReSidential And Commercial
    property_listing_name=models.CharField(max_length=300)
    position = models.IntegerField()

    def __str__(self):
        return self.property_listing_name

class Property_Listing_Type(models.Model): #Rental, Sales, Buy, Lease etc.
    type_of_listing=models.ForeignKey(to=Propertylisting_type, on_delete=models.CASCADE)
    listing_type=models.CharField(max_length=300)
    user_listing_type = models.CharField(max_length=300, null=True, blank=True)
    listing_position= models.CharField(max_length=300)
    is_active= models.BooleanField(default=True)

    def __str__(self):
        return self.listing_type

class Property_Main_Category(models.Model):
    listing_type= models.ForeignKey(Property_Listing_Type,on_delete=models.SET_NULL,null=True)
    Main_category  = models.CharField(max_length = 300)
    category_position= models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.Main_category
    

class Property_Sub_Category(models.Model):
    property_main_category = models.ForeignKey(to = Property_Main_Category, on_delete=models.SET_NULL,null=True)
    category_position= models.IntegerField()
    property_sub_category_Name = models.CharField(max_length = 300)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.property_sub_category_Name

class Property_Type(models.Model):
    property_sub_category = models.ForeignKey(to = Property_Sub_Category, on_delete=models.CASCADE)
    property_type_image = models.ImageField(upload_to="Property-Type")
    proprty_type_name = models.CharField(max_length=300)
    category_position= models.IntegerField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.proprty_type_name

class Amenities_Master(models.Model):
    amenities_icon = models.ImageField(upload_to='Amenities_icon')
    amenities_name = models.CharField(max_length = 300)
    position = models.IntegerField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.amenities_name

class Property_Detail(models.Model):
    property_listing_type=models.ForeignKey(to=Propertylisting_type, on_delete=models.SET_NULL,null=True,blank=True)
    propertylisting_type=models.ForeignKey(to=Property_Listing_Type, on_delete=models.SET_NULL,null=True,blank=True)
    slug=models.SlugField(max_length=500,unique=True, null=True, blank=True)
    property_title = models.CharField(max_length=300,null=True,blank=True)
    propert_description = models.TextField(null=True,blank=True)
    property_main_image = models.FileField(upload_to='Property_main_image',null=True,blank=True)
    property_main_floor_plan = models.FileField(upload_to='Property_main_floor_plan',null=True,blank=True)
    property_main_category = models.ForeignKey(to=Property_Main_Category, on_delete=models.SET_NULL, null=True, blank=True)
    property_sub_category = models.ForeignKey(to = Property_Sub_Category, on_delete=models.SET_NULL, null=True, blank=True)
    property_type = models.ForeignKey(to = Property_Type, on_delete=models.SET_NULL, null=True, blank=True)
    property_address_1 = models.TextField(null=True,blank=True)
    property_address_2 = models.TextField(null=True,blank=True)
    property_area=models.ForeignKey(to=AreaMaster,on_delete=models.SET_NULL,null=True,blank=True)
    property_city = models.ForeignKey(to=CityMaster,on_delete=models.SET_NULL,null=True,blank=True)
    property_state = models.ForeignKey(to=StateMaster,on_delete=models.SET_NULL,null=True,blank=True)
    property_zip = models.CharField(max_length=300, null=True,blank=True)
    property_terms = models.CharField(max_length=300,null=True,blank=True)
    property_offer = models.CharField(max_length=300,null=True,blank=True)
    is_property_fee = models.BooleanField(default=False,null=True,blank=True)
    fees = models.CharField(max_length=300,null=True,blank=True)
    SellerAgency = models.CharField(max_length=300,null=True,blank=True)
    BuyerAgency = models.CharField(max_length=300,null=True,blank=True)
    property_listing_amount = models.FloatField(null=True,blank=True)
    property_cost_per_sq=models.IntegerField(null=True, blank=True)
    created_date = models.DateField(auto_now_add = True, null=True, blank=True)
    created_time = models.TimeField(auto_now_add = True, null=True, blank=True)
    user_profile = models.ForeignKey(to=UserProfile, on_delete=models.SET_NULL,null=True,blank=True)
    property_pet_friendly=models.BooleanField(default=False,null=True,blank=True)
    min_30_shows=models.BooleanField(default=False,null=True,blank=True)
    open_house=models.BooleanField(default=False,null=True,blank=True)
    No_sure_Pet_allowed=models.BooleanField(default=True,null=True,blank=True)

    Bedrooms=models.IntegerField(null=True,blank=True)
    Bathrooms=models.IntegerField(null=True,blank=True)
    Square_sqft=models.IntegerField(null=True,blank=True)
    Exterior_Sqft=models.IntegerField(null=True,blank=True)
    Maintence_fee=models.IntegerField(null=True,blank=True)
    Real_Estate_Tax=models.IntegerField(null=True,blank=True)
    Financing=models.IntegerField(null=True,blank=True)
    Minimum_Down=models.IntegerField(null=True,blank=True)
    Units=models.IntegerField(null=True,blank=True)
    Rooms=models.IntegerField(null=True,blank=True)
    Block=models.IntegerField(null=True,blank=True)
    Lot=models.IntegerField(null=True,blank=True)
    Zone=models.IntegerField(null=True,blank=True)
    Building_Sqft=models.IntegerField(null=True,blank=True)
    Lot_Dimensions=models.IntegerField(null=True,blank=True)
    Building_Dimension=models.IntegerField(null=True,blank=True)
    Stories=models.IntegerField(null=True,blank=True)
    FAR=models.IntegerField(null=True,blank=True)
    Assessment=models.IntegerField(null=True,blank=True)
    Annual_Taxes=models.IntegerField(null=True,blank=True)
    Available_Air_Rights=models.IntegerField(null=True,blank=True)
    
    Apt=models.CharField(max_length=300,null=True,blank=True)
    is_property_open=models.BooleanField(default=True)
    is_property_expired = models.BooleanField(default = False)
    is_property_exclusive = models.BooleanField(default=False)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.property_title
    
def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(rl_pre_save_receiver, sender=Property_Detail)

class PetProperty(models.Model):
    pet_master=models.ForeignKey(to=PetMaster,on_delete=models.CASCADE)
    property_details = models.ForeignKey(to=Property_Detail, on_delete= models.CASCADE)
    created_date = models.DateTimeField(auto_now_add = True, null=True, blank=True)

class Property_Amenities(models.Model):
    amenites_master = models.ForeignKey(to= Amenities_Master, on_delete = models.CASCADE)
    property_details = models.ForeignKey(to=Property_Detail, on_delete= models.CASCADE)
    amenities_value = models.CharField(max_length=300)
    created_date = models.DateTimeField(auto_now_add = True, null=True, blank=True)

    def __str__(self):
        return self.amenities_value

class Property_listing_event(models.Model):
    property_details = models.ForeignKey(to=Property_Detail, on_delete=models.CASCADE)
    property_listing_start_date = models.DateTimeField(null=True,blank=True)
    property_listing_end_date = models.DateTimeField(null=True,blank=True)

class Property_Image(models.Model):
    property_detail_id=models.ForeignKey(to=Property_Detail, on_delete=models.CASCADE)
    property_image_type = models.CharField(max_length=300, null=True, blank=True)
    property_image= models.ImageField(upload_to="property_image")
    is_active = models.BooleanField(default=True)

class Guest_Users_Save_Listing(models.Model):
    property_details = models.ForeignKey(to=Property_Detail, on_delete=models.CASCADE)  
    user=models.ForeignKey(to=User, on_delete=models.CASCADE)
    is_property_available = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=0)

class Seen_Property_listing(models.Model):
    property_detail_id=models.ForeignKey(to=Property_Detail, on_delete=models.CASCADE)
    user_profile_id=models.ForeignKey(to=User, on_delete=models.CASCADE)

class filter_save_serach(models.Model):
    filterName = models.CharField(max_length=300,null=True, blank=True)
    user=models.ForeignKey(to=User, on_delete=models.CASCADE,blank=True, null=True)
    Type = models.ForeignKey(to=Property_Listing_Type, on_delete=models.CASCADE,blank=True, null=True)
    propertymaincategory=models.ForeignKey(to=Property_Main_Category, on_delete=models.CASCADE,blank=True, null=True)
    propertysubcategory=models.ForeignKey(to=Property_Sub_Category, on_delete=models.SET_NULL, null=True, blank=True)
    Bedrooms=models.CharField(max_length=300,null=True, blank=True)
    Bathrooms=models.CharField(max_length=300,null=True, blank=True)
    units=models.CharField(max_length=300,null=True, blank=True)
    room=models.CharField(max_length=300,null=True, blank=True)
    monthly=models.BooleanField(null=True, blank=True)
    cost_per_square_fit=models.BooleanField(null=True, blank=True)
    block=models.CharField(max_length=300,null=True, blank=True)
    lot=models.CharField(max_length=300,null=True, blank=True)
    Zone=models.CharField(max_length=300,null=True, blank=True)
    lot_diamensions=models.CharField(max_length=300,null=True, blank=True)
    building_diamensions=models.CharField(max_length=300,null=True, blank=True)
    stories=models.CharField(max_length=300,null=True, blank=True)
    far=models.CharField(max_length=300,null=True, blank=True)
    Assessment=models.CharField(max_length=300,null=True,blank=True)
    Annual_Taxes=models.CharField(max_length=300,null=True,blank=True)
    Available_Air_Rights=models.CharField(max_length=300,null=True,blank=True)
    Squft_min=models.IntegerField(null=True, blank=True)
    Squft_max=models.IntegerField(null=True, blank=True)
    Price_Min=models.IntegerField(null=True, blank=True)
    Price_Max=models.IntegerField(null=True, blank=True)
    Amenities_filter=models.JSONField(null=True, blank=True)
    area=models.ForeignKey(to=AreaMaster, on_delete=models.SET_NULL, blank=True, null=True)
    city=models.ForeignKey(to=CityMaster, on_delete=models.SET_NULL, blank=True, null=True)
    state=models.ForeignKey(to=StateMaster, on_delete=models.SET_NULL, blank=True, null=True)
    country=models.ForeignKey(to=CountryMaster, on_delete=models.SET_NULL, blank=True, null=True)

class LuxarySalesAmt(models.Model):
    Amt=models.IntegerField()
    date=models.DateField(auto_now_add=True)
    time=models.TimeField(auto_now_add=True)

class LuxaryRentAmt(models.Model):
    Amt=models.IntegerField()
    date=models.DateField(auto_now_add=True)
    time=models.TimeField(auto_now_add=True)

# Invitations Link Token Based
import secrets
import datetime

class Invitation(models.Model):
    userid=models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()
    token = models.CharField(max_length=64, default=secrets.token_hex)
    expiration_date = models.DateTimeField(null=True,blank=True)
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    license = models.CharField(max_length=300)
    is_accept = models.BooleanField(default=False)
    
    def __str__(self):
        return self.first_name
    # def save(self, *args, **kwargs):
    #     # Set the expiration date to the current date plus the desired number of hours
    #     self.expiration_date = datetime.datetime.now() + datetime.timedelta(hours=3)
    #     super().save(*args, **kwargs)

class TeamProperty(models.Model):
    userprofile_id = models.ForeignKey(to = UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    propertydetail_id = models.ForeignKey(to = Property_Detail, on_delete=models.SET_NULL, null=True, blank=True)

class ContactNow(models.Model):
    userid = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    userprofile_id = models.ForeignKey(to=UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    property_id = models.ForeignKey(to = Property_Detail, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField(null=True, blank = True)

class Property30minshow(models.Model):
    Monday = models.JSONField(null=True, blank = True)
    Tuesday = models.JSONField(null=True, blank = True)
    Wednesday = models.JSONField(null=True, blank = True)
    Thursday = models.JSONField(null=True, blank = True)
    Friday = models.JSONField(null=True, blank = True)
    Saturday = models.JSONField(null=True, blank = True)
    Sunday = models.JSONField(null=True, blank = True)
    property_details = models.ForeignKey(to=Property_Detail, on_delete= models.CASCADE)
    created_date = models.DateTimeField(auto_now_add = True, null=True, blank=True)

class Property_Space_Availability(models.Model):
    Property = models.ForeignKey(to=Property_Detail, on_delete= models.CASCADE)
    space = models.CharField(max_length=300, null = True, blank = True)
    size = models.CharField(max_length=300, null = True, blank = True)
    term = models.CharField(max_length=300, null = True, blank = True)
    rate = models.CharField(max_length=300, null = True, blank = True)
    type = models.CharField(max_length=300, null = True, blank = True)

class OpenHouseProperty(models.Model):
    Monday = models.JSONField(null=True, blank = True)
    Tuesday = models.JSONField(null=True, blank = True)
    Wednesday = models.JSONField(null=True, blank = True)
    Thursday = models.JSONField(null=True, blank = True)
    Friday = models.JSONField(null=True, blank = True)
    Saturday = models.JSONField(null=True, blank = True)
    Sunday = models.JSONField(null=True, blank = True)
    property_details = models.ForeignKey(to=Property_Detail, on_delete= models.CASCADE)
    created_date = models.DateTimeField(auto_now_add = True, null=True, blank=True)

class Review(models.Model):
    AgentUser = models.ForeignKey(to = UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(to = User, on_delete=models.CASCADE, null=True, blank=True)
    meet = models.BooleanField(null=True, blank=True)
    Knowledge = models.IntegerField(default=0)
    Professionalism = models.IntegerField(default=0)
    Customer_Service = models.IntegerField(default=0)
    Respectful = models.IntegerField(default=0)
    Recommend = models.IntegerField(default=0)
    experience = models.TextField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True)

class Terms(models.Model):
    property_listing_type=models.ForeignKey(to=Propertylisting_type, on_delete=models.SET_NULL,null=True,blank=True)
    propertylisting_type=models.ForeignKey(to=Property_Listing_Type, on_delete=models.SET_NULL,null=True,blank=True)
    usertypeobj = models.IntegerField(null=True, blank=True)
    terms = models.TextField(null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)

class Offer(models.Model):
    property_listing_type=models.ForeignKey(to=Propertylisting_type, on_delete=models.SET_NULL,null=True,blank=True)
    propertylisting_type=models.ForeignKey(to=Property_Listing_Type, on_delete=models.SET_NULL,null=True,blank=True)
    usertypeobj = models.IntegerField(null=True, blank=True)
    offer = models.TextField(null = True, blank=True)
    position = models.IntegerField(null = True, blank = True)

class Document(models.Model):
    user = models.ForeignKey(to = User, related_name='doc_owner_set', on_delete=models.CASCADE, null=False, blank = False)
    share_from = models.ForeignKey(to = User, related_name='doc_viewer_set', on_delete=models.CASCADE, null=True, blank = True)
    signed_to =  models.ForeignKey(to = User, related_name='doc_user_set', on_delete=models.CASCADE, null=True, blank = True)
    filename = models.CharField(max_length = 100, null = True, blank = True)
    file = models.FileField(upload_to='uploaded_files/documents', null=True, blank = True)
    shared = models.BooleanField(default=False)
    signed = models.BooleanField(default=False)
    signing = models.IntegerField(null=True, blank=True)
    share_with = ArrayField(models.CharField(max_length=200),null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    position = models.PositiveIntegerField(default=0)