from django.db import models
from accounts.models import *
from master.models import *
from property.models import *
from django.utils.text import slugify
import string
from django.db.models.signals import pre_save
from .util import unique_virtual_slug_generator
from django.core.validators import MaxLengthValidator, MinLengthValidator
import secrets

class VirtualOffice(models.Model):
    userprofile = models.ForeignKey(to = UserProfile, on_delete=models.CASCADE, null = True, blank = True)
    virtual_office_name = models.CharField(max_length=300, null=True, blank=True)
    slug=models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.virtual_office_name

def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_virtual_slug_generator(instance)

pre_save.connect(rl_pre_save_receiver, sender=VirtualOffice)


class VirtualOfficeTeam(models.Model):
    virtualid = models.ForeignKey(to =VirtualOffice, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    is_status = models.BooleanField(null=True, blank=True)
    is_request = models.BooleanField(default=True,null=True, blank=True)
    expiration_date = models.DateField(null=True,blank=True)
    token = models.CharField(max_length=64, default=secrets.token_hex)
    member_type = models.CharField(max_length=300, null = True, blank=True)

class customer_info(models.Model):
    user = models.ForeignKey(VirtualOfficeTeam, on_delete=models.SET_NULL, null=True, blank=True)
    origin_email = models.EmailField(null=True, blank=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    contact_no_1 = models.CharField(max_length=300, null=True, blank=True)
    contact_no_2 = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    towns_of_interest = models.CharField(max_length=300, null=True, blank=True)
    date_of_close = models.DateField(null=True, blank=True)
    current_address = models.TextField(null=True, blank=True)
    purchase_rental_price = models.CharField(max_length=300, null=True, blank=True)
    martial_status = models.CharField(max_length=200, null=True, blank= True)
    relationship = models.CharField(max_length=200, null=True, blank= True)
    doc1 = models.FileField(upload_to="cunstomer_doc_1", null=True, blank=True)
    doc2 = models.FileField(upload_to="cunstomer_doc_2", null=True, blank=True)
    doc3 = models.FileField(upload_to="cunstomer_doc_3", null=True, blank=True)
    add_note = models.TextField(null=True, blank=True)
    is_edit = models.BooleanField(default=False)

class VirtualOfficeProperty(models.Model):
    userprofile = models.ForeignKey(to = UserProfile,on_delete=models.SET_NULL, null=True, blank=True) # aent
    virtualofficeid = models.ForeignKey(to =VirtualOffice, on_delete=models.SET_NULL, null=True, blank=True)
    propertyid = models.ForeignKey(to=Property_Detail,  on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(to = User,on_delete=models.SET_NULL, null=True, blank=True) # Customer
    note = models.TextField(null=True, blank=True)
    is_like = models.BooleanField(null=True, blank=True)
    is_dislike = models.BooleanField(null=True, blank=True)



# class NoteOnVirtualOfficeProperty(models.Model):
#     user = models.ForeignKey(to = User,on_delete=models.SET_NULL, null=True, blank=True)
#     propertyid = models.ForeignKey(to=Property_Detail,  on_delete=models.SET_NULL, null=True, blank=True)
#     note = models.TextField(null=True, blank=True)
#     is_like = models.BooleanField(null=True, blank=True)
#     is_dislike = models.BooleanField(null=True, blank=True)
#     virtual_office = models.ForeignKey(to =VirtualOffice, on_delete=models.SET_NULL, null=True, blank=True)

class Signed_Documnets_Custom_Info(models.Model):
    virtualoffice = models.ForeignKey(to = VirtualOffice, on_delete=models.SET_NULL, null=True, blank=True)
    customobj = models.ForeignKey(to = customer_info, on_delete=models.SET_NULL, null=True, blank=True)
    filename = models.CharField(max_length=300, null=True, blank=True)
    doc = models.FileField(upload_to="uploaded_files/documents", null=True, blank=True)
    shared = models.BooleanField(default=True, null=True, blank=True)
    signed = models.BooleanField(default=False, null=True, blank=True)
