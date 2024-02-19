from django.db import models
from accounts.models import User,UserProfile
from property.models import Property_Detail
from master.models import *

# Create your models here.

class BoostMarketingServicesTOUser(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    ServiceNumber = models.IntegerField()
    is_active = models.BooleanField(default=True)

class Plan_Type(models.Model):
    plan_type = models.IntegerField(null=True, blank=True)
    top_description = models.TextField(null=True, blank=True)
    termsandservices = models.TextField(null=True, blank=True)

class BoostMarkitingPlan(models.Model):
    plan_type = models.IntegerField(null=True, blank=True)
    impression = models.CharField(max_length=300, null=True, blank=True)
    cost = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    # termsandservices = models.TextField(null=True, blank=True)

class BoostMarketingTable(models.Model):
    user=models.ForeignKey(to=User,on_delete=models.CASCADE)
    boostbarkitingplan=models.ForeignKey(to=BoostMarkitingPlan,on_delete=models.CASCADE,null=True, blank=True)
    CampaignName=models.CharField(max_length=300)
    requested_date=models.DateField(null=True, blank=True)
    start_date=models.DateField(null=True, blank=True)
    end_date=models.DateField(null=True, blank=True)
    url=models.CharField(max_length=300,null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    # area=models.ForeignKey(to=AreaMaster,on_delete=models.CASCADE,null=True, blank=True)
    # city=models.ForeignKey(to=CityMaster,on_delete=models.CASCADE,null=True, blank=True)
    # StateMaster=models.ForeignKey(to=StateMaster,on_delete=models.CASCADE,null=True, blank=True)
    # CountryMaster=models.ForeignKey(to=CountryMaster,on_delete=models.CASCADE,null=True, blank=True)
    Image=models.FileField(null=True, blank=True)
    message=models.TextField(null=True, blank=True)
    keyword=models.JSONField(null=True, blank=True)
