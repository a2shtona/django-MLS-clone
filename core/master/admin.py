from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(CountryMaster)
@admin.register(CouponAndPromo)
class Admin_CouponAndPromo(admin.ModelAdmin):
    list_display = ['id','name','couponcode','startdate','enddate','number_of_user']

@admin.register(SubscriptionPlanServices)
class Admin_SubscriptionPlanServices(admin.ModelAdmin):
    list_display = ['id','Name','plan_type','monthly_price','yearly_price','discounttype','discount','discountmininumseat','subscriptionservices','is_active','total_listing','propertype','properlisting']

admin.site.register(AreaMaster) 
admin.site.register(LanguageMaster)
admin.site.register(HomeCard)



admin.site.register(Propetyexcelfile)
admin.site.register(Locationexcelfile)
admin.site.register(Languageexcelfile)
admin.site.register(StateMaster)
admin.site.register(CityMaster)
admin.site.register(ZipCodeMaster)
admin.site.register(SubscriptionServices)
admin.site.register(PetMaster)
admin.site.register(HomeCardTitle)
