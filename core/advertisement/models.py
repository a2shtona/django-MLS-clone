from django.db import models

# Create your models here.


# class AdvertismentUser(models.Model):
#     first_name = models.CharField(max_length=100, null=True, blank=True)
#     last_name=models.CharField(max_length=100, null=True, blank=True)
#     email=models.EmailField(max_length=100, null=True, blank=True)
#     password=models.CharField(max_length=100, null=True, blank=True)
#     date_joined=models.DateField(null=True, blank=True)
#     last_login=models.DateField(null=True, blank=True)
#     AdvertismentUser_id=models.CharField(max_length=100, null=True, blank=True, unique=True)
#     is_active=models.BooleanField(null=True, blank=True, default=False)

class AdvertismentUser(models.Model):
    Business_Name = models.CharField(max_length=300, null=True, blank=True)
    Business_Phone=models.CharField(max_length=300, null=True, blank=True)
    Business_Email=models.EmailField(max_length=300, null=True, blank=True)
    password=models.CharField(max_length=300, null=True, blank=True)
    Industry = models.CharField(max_length=300, null=True, blank=True)
    date_joined=models.DateField(null=True, blank=True)
    last_login=models.DateField(null=True, blank=True)
    AdvertismentUser_id=models.CharField(max_length=300, null=True, blank=True, unique=True)
    is_active=models.BooleanField(null=True, blank=True, default=False)

class Advertisement(models.Model):
    AdvertismentUser_id=models.ForeignKey(to=AdvertismentUser, on_delete=models.CASCADE, null=True, blank=True)
    Image=models.FileField(upload_to='AdvertismentImage', null=True, blank=True )
    description=models.TextField(null=True, blank=True)
    date=models.DateField(null=True, blank=True)
    advertisment_start_date=models.DateField(null=True, blank=True)
    advertisment_end_date=models.DateField(null=True, blank=True)
    title=models.CharField(null=True, blank=True, max_length=300)
    status=models.IntegerField(null=True, blank=True, default=False)
    is_approved=models.BooleanField(null=True, blank=True, default=False)
    is_approved_date=models.DateField(null=True, blank=True)
    is_suspended=models.BooleanField(null=True, blank=True, default=False)
