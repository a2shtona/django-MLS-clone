from rest_framework import serializers
from accounts.models import *
from accounts.serializers import *
from property.models import *
from property.serializer import *

class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()
    class Meta:
        model=User
        fields = ["id","first_name", "last_name", "username", "last_login", "date_joined", "is_active", "is_email_verified", "is_suspended", "is_social","user_type"]
    
    def get_user_type(self, obj):
        usertype = UserType.objects.get(user = obj.id)
        return usertype.user_type

class UserTypeUserSerializer(serializers.ModelSerializer):
    user = UserLoginSerializer()
    class Meta:
        model = UserType
        fields = "__all__"

class UserProfileListingSerializer(serializers.ModelSerializer):
    user_type = UserTypeUserSerializer()
    class Meta:
        model = UserProfile
        fields = "__all__"

class AreaNbSpecilitySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    area_id = serializers.SerializerMethodField()
    class Meta:
        model = Nb_specality_area
        fields="__all__"
    
    def get_area_id(self, obj):
        areaname = []
        areaid = AreaMaster.objects.filter(id__in = obj.area_id)
        for i in areaid:
            areaname.append(i.area_name)
        return areaname

class AgentLicAdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = AgentLic
        fields = "__all__"

class SupportticketAdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model= SupportTickets
        fields = "__all__"

class GetAdminTermsSerilizer(serializers.ModelSerializer):
    property_listing_type = Propertylisting_typeViewSerializer()
    propertylisting_type = Property_listing_typeViewSerializer()
    class Meta:
        model = Terms
        fields = '__all__'

class GetAdminOfferSerilizer(serializers.ModelSerializer):
    property_listing_type = Propertylisting_typeViewSerializer()
    propertylisting_type = Property_listing_typeViewSerializer()
    class Meta:
        model = Offer
        fields = '__all__'

class AgentLicAdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = AgentLic
        fields = "__all__"

class Property_listing_typeViewAdminSerializer(serializers.ModelSerializer):
    type_of_listing = Propertylisting_typeViewSerializer()
    class Meta:
        model=Property_Listing_Type
        fields="__all__"

class PropertyMainAdminCategorySerializer(serializers.ModelSerializer):
    listing_type = Property_listing_typeViewAdminSerializer()
    class Meta:
        model=Property_Main_Category
        fields="__all__"

class PropertySubCategoryAdminSerializer(serializers.ModelSerializer):
    property_main_category = PropertyMainAdminCategorySerializer()
    class Meta:
        model=Property_Sub_Category
        fields="__all__"