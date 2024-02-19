from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(BoostMarkitingPlan)
admin.site.register(BoostMarketingServicesTOUser)
admin.site.register(BoostMarketingTable)

@admin.register(Plan_Type)
class Plan_Admin(admin.ModelAdmin):
    list_display = ['id','plan_type','top_description','termsandservices']