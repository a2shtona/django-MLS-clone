from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register(Property_Type)
admin.site.register(Property_Amenities)
admin.site.register(Property_listing_event)
admin.site.register(LuxarySalesAmt)

@admin.register(Invitation)
class Invitation_Admin(admin.ModelAdmin):
    list_display = ['id','userid','email','token','expiration_date','first_name',
                    'last_name','license','is_accept']

admin.site.register(Guest_Users_Save_Listing)

@admin.register(Propertylisting_type)
class Propertylisting_type_Admin(admin.ModelAdmin):
    list_display = ['id','property_listing_name','position']

@admin.register(Property_Detail)
class Property_Details_Admin(admin.ModelAdmin):
    list_display=[
        'id','property_listing_type','property_title','property_main_category','property_sub_category',
        'property_type','property_area','property_city','property_state','property_zip','is_property_fee',
        'property_pet_friendly','created_date','user_profile'
    ]

@admin.register(Property_Image)
class Property_ImageAdmin(admin.ModelAdmin):
    list_display = [
        'id','property_detail_id'
    ]
admin.site.register(Property_Sub_Category)
admin.site.register(Seen_Property_listing)
@admin.register(Property_Main_Category)
class PropertyMainCategory(admin.ModelAdmin):
    list_display = ['id','Main_category']
admin.site.register(filter_save_serach)

@admin.register(Property_Listing_Type)
class Property_Listing_Admin(admin.ModelAdmin):
    list_display = ['id','type_of_listing','listing_type','is_active']

@admin.register(Property30minshow)
class Property30minshowAdmin(admin.ModelAdmin):
    list_display = ["id", "Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday","property_details"]

@admin.register(TeamProperty)
class TeamPropertyAdmin(admin.ModelAdmin):
    list_display = ["id", "userprofile_id","propertydetail_id"]

admin.site.register(Review)
admin.site.register(Amenities_Master)
admin.site.register(PetProperty)
admin.site.register(LuxaryRentAmt)
admin.site.register(ContactNow)
admin.site.register(Property_Space_Availability)
admin.site.register(OpenHouseProperty)
admin.site.register(Terms)
admin.site.register(Offer)
admin.site.register(Document)
