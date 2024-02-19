from rest_framework import serializers
from .models import *



# Registration
# class AdvertismentRegistrationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AdvertismentUser
#         fields =['id', 'first_name', 'last_name', 'email','date_joined', 'last_login', 'AdvertismentUser_id','is_active']

class AdvertismentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertismentUser
        fields =['id', 'Business_Name', 'Business_Phone', 'Business_Email','date_joined', 'last_login', 'AdvertismentUser_id','is_active','Industry']
 
class AdvertismentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields="__all__"