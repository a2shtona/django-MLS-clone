from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# from ckeditor.fields import RichTextField
from macaddress.fields import MACAddressField
from PIL import Image
from master.models import *

from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.db.models.signals import pre_save
from .utils import unique_slug_generator    


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    send_mail(
        # title:
        "Password Reset for {title}".format(title="MLS-tutor.com"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )   



class UserManager(BaseUserManager):
    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user

class User(AbstractUser):
    is_active=models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)
    is_social = models.BooleanField(default=False)

    

class UserType(models.Model):
    user=models.OneToOneField(to=User,on_delete=models.CASCADE, null=True)
    user_type=models.IntegerField()

class UserProfile(models.Model):
    slug=models.SlugField(max_length=300,unique=True, null=True, blank=True)
    user_type=models.OneToOneField(unique=True,to=UserType,on_delete=models.CASCADE,null=True, blank=True)
    first_name=models.CharField(max_length=300,null=True, blank=True)
    last_name=models.CharField(max_length=300,null=True, blank=True)
    work_number_1=models.CharField(max_length=300,null=True, blank=True)
    work_number_2=models.CharField(max_length=300,null=True, blank=True)
    cell_number=models.CharField(max_length=300,null=True, blank=True)
    is_work_numer_1_valid=models.BooleanField(default=False)
    type_of_account=models.IntegerField(null=True, blank=True)
    profile_image=models.ImageField(upload_to='profile_pictures',null=True,blank=True)
    cover_image=models.ImageField(upload_to='cover_pictures',null=True,blank=True)
    brokerage_name=models.CharField(max_length=300,null=True, blank=True)
    sales_persones_license=models.CharField(max_length=300,null=True, blank=True)
    agent_broker_license_title=models.CharField(max_length=300,null=True, blank=True)
    create_team=models.BooleanField(null=True, blank=True)
    team_name=models.CharField(max_length=300,null=True, blank=True)
    languages=models.JSONField(null=True, blank=True)
    linkedin_url=models.URLField(max_length=300,null=True, blank=True)
    twitter_url=models.URLField(max_length=300,null=True, blank=True)
    facebook_url=models.URLField(max_length=300,null=True, blank=True)
    instagram_url=models.URLField(max_length=300,null=True, blank=True)
    tiktok_url=models.URLField(max_length=300,null=True, blank=True)
    youtube=models.URLField(max_length=300,null=True, blank=True)
    personal_bio=models.TextField(null=True, blank=True)
    is_profilepassword=models.BooleanField(null=True, blank=True)
    profile_password=models.CharField(max_length=300,null=True, blank=True)
    name_of_business_listing=models.CharField(max_length=300, null=True, blank=True)
    business_id=models.CharField(max_length=300,null=True, blank=True)
    addition_user=models.CharField(max_length=300, null=True, blank=True)
    number_user=models.IntegerField(null=True, blank=True)
    address_line_1=models.CharField(max_length=300, null=True, blank=True)
    address_line_2=models.CharField(max_length=300, null=True, blank=True)
    areamaster=models.ForeignKey(to=AreaMaster,null=True, blank=True,on_delete=models.SET_NULL)
    citymaster=models.ForeignKey(to=CityMaster,null=True, blank=True,on_delete=models.SET_NULL)
    state=models.ForeignKey(to=StateMaster,null=True, blank=True,on_delete=models.SET_NULL)
    # zip_code=models.ForeignKey(to=ZipCodeMaster,null=True, blank=True,on_delete=models.SET_NULL)
    zip_code=models.CharField(max_length=300, null=True, blank=True)
    nickname=models.CharField(max_length=300)
    unique_id = models.CharField(max_length=300, null=True, blank=True)
    listing_count = models.PositiveIntegerField(default=0)
    rating = models.PositiveIntegerField(default=0)
    time_zone = models.CharField(max_length=300, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save()  # saving image first
        if self.profile_image:
            img = Image.open(self.profile_image.path) # Open image using self
            if img.height > 1080 or img.width > 1080:
                new_img = (1080,1080)
                img.thumbnail(new_img)
                img.save(self.profile_image.path)  # saving image at the same path


def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.first_name != None and instance.last_name != None:
        if not instance.slug:
            instance.slug = unique_slug_generator(instance)
    else:
        instance.slug=None

pre_save.connect(rl_pre_save_receiver, sender=UserProfile)


class User_Log(models.Model):
    user_type = models.ForeignKey(to=UserType, on_delete=models.CASCADE)
    action_type = models.BooleanField(default=False)
    date_time = models.DateTimeField()
    ip_address = models.GenericIPAddressField()
    longitude = models.CharField(max_length=300)
    latitude = models.CharField(max_length=300)
    mac_address = MACAddressField()
    location = models.TextField()


class AgentLic(models.Model):
    user=models.OneToOneField(to=User, on_delete=models.CASCADE,null=True, blank=True)
    license_number=models.CharField(max_length=300, null=True, blank=True)
    Full_name = models.CharField(max_length=300, null=True, blank=True)
    first_name=models.CharField(max_length=300, null=True, blank=True)
    last_name=models.CharField(max_length=300, null=True, blank=True)
    is_validated=models.BooleanField(default=False)
    is_requested=models.BooleanField(default=False)
    lic_already_use=models.BooleanField(default=False)
    lic_Type=models.CharField(max_length=300, blank=True, null=True)
    brokerage_name=models.CharField(max_length=300,null=True, blank=True)
    is_rejected = models.BooleanField(null=True, blank=True)

class AccountSetting(models.Model):
    user=models.ForeignKey(to=User, on_delete=models.CASCADE)
    type_allowed=models.IntegerField(null=True,blank=True) #0-Residential 1-Commercial 2-both
    email_notification=models.BooleanField(default=False)
    text_notification=models.BooleanField(default=False)

class AgentApprovedSubscriptionPlan(models.Model):
    user=models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    plan_id=models.ForeignKey(to=SubscriptionPlanServices, on_delete=models.CASCADE, null=True, blank=True)   
    requested_date=models.DateField(null=True, blank=True)
    approved_date=models.DateField(null=True, blank=True)
    next_billing_date=models.DateField(null=True, blank=True)
    status=models.BooleanField(default=True)
    plan_choices=models.CharField(max_length=300, null=True, blank=True)

# class Nb_specality_area(models.Model):
#     user=models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
#     area_id=models.ForeignKey(to = AreaMaster, on_delete=models.CASCADE, null=True, blank=True)
#     doc1=models.FileField(upload_to='nb_sp_area',null=True, blank=True)
#     doc2=models.FileField(upload_to='nb_sp_area',null=True, blank=True)
#     doc3=models.FileField(upload_to='nb_sp_area',null=True, blank=True)    

approve_choise=(
    ("Approve","Approve"),
    ("Reject","Reject"),
    ("Pending","Pending")
    )


class Nb_specality_area(models.Model):
    user=models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    area_id=models.JSONField(null=True, blank=True)
    doc1=models.FileField(upload_to='nb_sp_area',null=True, blank=True)
    doc2=models.FileField(upload_to='nb_sp_area',null=True, blank=True)
    doc3=models.FileField(upload_to='nb_sp_area',null=True, blank=True)
    is_requested=models.BooleanField(default=False)
    is_verified = models.CharField(
        max_length=256, choices=approve_choise,null=True, blank=True, default="Pending"
    )

class SupportTickets(models.Model):
    user=models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    ticket_no=models.CharField(max_length=300, unique=True)
    issue_type=models.CharField(max_length=300)
    title=models.CharField(max_length=300)
    description=models.TextField()
    priority=models.CharField(max_length=300)
    image=models.FileField(upload_to="supportticket",null=True, blank=True)
    status=models.BooleanField(null= True, blank=True)
    is_request = models.BooleanField(default=True)
    reported_date=models.DateField(null=True,blank=True)
    comments=models.TextField(null=True, blank=True)

class IssueType(models.Model):
    issue_type=models.CharField(max_length=300)
    position=models.IntegerField()

class IssuePriority(models.Model):
    priority=models.CharField(max_length=300)
    position=models.IntegerField()

class Card(models.Model):
    user=models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    card_name=models.CharField(max_length=300, null= True, blank=True)
    # card_number=models.BigIntegerField(null=True, blank=True)
    card_number=models.CharField(max_length=300,null=True, blank=True)
    month=models.IntegerField(null=True, blank=True)
    year=models.IntegerField(null=True, blank=True)
    cvc=models.CharField(max_length=300,null=True, blank=True)

class Billing(models.Model):
    user=models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    card_id=models.ForeignKey(to=Card, on_delete=models.CASCADE, null=True, blank=True)
    First_Name=models.CharField(max_length=300, null=True, blank=True)
    Last_Name=models.CharField(max_length=300, null=True, blank=True)
    Phone_number=models.CharField(max_length=300,null=True, blank=True)
    Address1=models.CharField(max_length=300, null=True, blank=True)
    Address2=models.CharField(max_length=300, null=True, blank=True)
    cityid=models.ForeignKey(to=CityMaster, on_delete=models.CASCADE, null=True, blank=True)
    stateid=models.ForeignKey(to=StateMaster, on_delete=models.SET_NULL, null=True, blank=True)
    # zipcodeid=models.ForeignKey(to=ZipCodeMaster, on_delete=models.SET_NULL, null=True, blank=True)
    zipcodeid=models.CharField(max_length=300,null=True, blank=True)
    Total_amount = models.CharField(max_length=300,null=True, blank=True)
    payment_date = models.DateField(null=True,blank=True)

class min_30(models.Model):
    userprofile = models.ForeignKey(to = UserProfile, on_delete = models.CASCADE, null= True, blank= True)
    Monday = models.JSONField(null=True, blank = True)
    Tuesday = models.JSONField(null=True, blank = True)
    Wednesday = models.JSONField(null=True, blank = True)
    Thursday = models.JSONField(null=True, blank = True)
    Friday = models.JSONField(null=True, blank = True)
    Saturday = models.JSONField(null=True, blank = True)
    Sunday = models.JSONField(null=True, blank = True)
    is_active = models.BooleanField(null=True, blank= True)

class Testmodel(models.Model):
    name = models.CharField(max_length=300, blank= True, null=True)

class SavedSalesPerosn(models.Model):
    user = models.ForeignKey(to = User, on_delete=models.SET_NULL, null=True, blank = True) # Guest User
    userprofile = models.ForeignKey(to = UserProfile, on_delete=models.SET_NULL, null=True, blank = True) # Sales Person Account