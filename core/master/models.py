from django.db import models
# Create your models here.

class Propetyexcelfile(models.Model):
    excel = models.FileField(upload_to="property_excel", null=True, blank=True)

class Locationexcelfile(models.Model):
    excel = models.FileField(upload_to="location_excel", null=True, blank=True)

class Languageexcelfile(models.Model):
    excel = models.FileField(upload_to="language_excel", null=True, blank=True)

class CountryMaster(models.Model):
    country_code=models.CharField(max_length=300)
    country_name=models.CharField(max_length=300)
    is_active=models.BooleanField(default=True)
    position=models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.country_name

class StateMaster(models.Model):
    country_master=models.ForeignKey(to=CountryMaster,on_delete=models.CASCADE)
    state_name=models.CharField(max_length=300)
    is_active=models.BooleanField(default=True)
    position=models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.state_name


class CityMaster(models.Model):
    state_master=models.ForeignKey(to=StateMaster,on_delete=models.CASCADE)
    city_name=models.CharField(max_length=300)
    city_image=models.ImageField(upload_to='City',null=True, blank=True)
    is_active=models.BooleanField(default=True)
    position=models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.city_name

class AreaMaster(models.Model):
    city_master=models.ForeignKey(to=CityMaster, on_delete=models.CASCADE)
    area_name = models.CharField(max_length=300)
    prefered_name = models.CharField(max_length=300, null=True, blank=True)
    is_active=models.BooleanField(default=True)
    position=models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.area_name

class ZipCodeMaster(models.Model):
    area_master=models.ForeignKey(to=AreaMaster, on_delete=models.CASCADE)
    Zipcode = models.CharField(max_length=300)
    is_active=models.BooleanField(default=True)
    position=models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.Zipcode
    
class LanguageMaster(models.Model):
    languages_name=models.CharField(max_length=255,unique=True)
    position=models.IntegerField()

    def __str__(self):
        return self.languages_name


class SubscriptionServices(models.Model):
    service_name=models.CharField(max_length=300)
    position=models.CharField(max_length=300)
    is_active = models.BooleanField(default=True)
    usertype = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.service_name

class CouponAndPromo(models.Model):
    name=models.CharField(max_length=300)
    couponcode=models.CharField(max_length=300)
    account_type=models.JSONField(max_length=300)
    startdate=models.DateField()
    enddate=models.DateField()
    couponfor=models.IntegerField()
    number_of_user=models.IntegerField()
    user_type=models.BooleanField()
    discount_type=models.BooleanField()
    discount=models.PositiveIntegerField()
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name
        
# PetMaster tabel
class PetMaster(models.Model):
    Pet_Image=models.ImageField(upload_to='Pet_Image')
    Pet_Name=models.CharField(max_length=300)
    is_active=models.BooleanField(default=True)
    position=models.IntegerField()
    position=models.IntegerField()

    def __str__(self):
        return self.Pet_Name

class SubscriptionPlans(models.Model):
    UserType=models.IntegerField()
    Name=models.CharField(max_length=300)
    plan_type= models.CharField(max_length=300)
    monthly_price= models.IntegerField()
    yearly_price= models.IntegerField()
    discounttype=models.BooleanField()
    discount= models.CharField(max_length=30)
    discountmininumseat=models.IntegerField()
    subscriptionservices=models.JSONField(null=True, blank=True)
    is_active= models.BooleanField(default=True)
    total_listing=models.IntegerField(null=True,blank=True)
    propertype=models.JSONField(null=True, blank=True)
    properlisting=models.JSONField(null=True, blank=True)
    titles=models.TextField(null=True, blank=True)
    
    def list_of_subscription_service(self):
        l=[]
        if self.subscriptionservices:
            for i in self.subscriptionservices:
                l.append(SubscriptionServices.objects.get(id=i))
        return l
    
    def __str__(self):
        return self.Name


class SubscriptionPlanServices(models.Model):
    UserType=models.IntegerField()
    Name=models.CharField(max_length=300)
    plan_type= models.CharField(max_length=300)
    monthly_price= models.IntegerField()
    yearly_price= models.IntegerField()
    discounttype=models.BooleanField()
    discount= models.CharField(max_length=300)
    discountmininumseat=models.IntegerField()
    subscriptionservices=models.JSONField()
    is_active= models.BooleanField(default=True)
    total_listing=models.IntegerField(null=True,blank=True)
    propertype=models.JSONField(null=True, blank=True)
    properlisting=models.JSONField(null=True, blank=True)
    listing_type=models.IntegerField(null=True, blank=True) #0-Residential 1-Commercial 2-Both
    titles=models.TextField(null=True, blank=True)
    Subscription_services=models.JSONField(null=True, blank=True)
    
    def list_of_subscription_service(self):
        l=[]
        if self.subscriptionservices:
            for i in self.subscriptionservices:
                l.append(SubscriptionServices.objects.get(id=i))
        return l
    
    def __str__(self):
        return self.Name

class HomeCardTitle(models.Model):
    Title=models.CharField(max_length=300,null=True,blank=True)
    Subtitle=models.CharField(max_length=300,null=True,blank=True)

    def __str__(self):
        return self.Title

class HomeCard(models.Model):
    Icon=models.ImageField(upload_to='HomeCardIcon')    
    Card_Title=models.CharField(max_length=300,null=True,blank=True)
    Card_body=models.CharField(max_length=300,null=True,blank=True)

    def __str__(self):
        return self.Card_Title
