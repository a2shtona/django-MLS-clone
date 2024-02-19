from rest_framework import serializers
from .models import *
from accounts.serializers import AgentProfileSerializer
from master.serializer import *
from accounts.serializers import *
from virtual_office.models import VirtualOfficeProperty

from django.db.models import Q

class PropertyMainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Property_Main_Category
        fields="__all__"

class PropertySubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Property_Sub_Category
        fields="__all__"

class AmenitiesNasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=Amenities_Master
        fields="__all__"


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Property_Image
        fields="__all__"

class Propertylisting_typeViewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Propertylisting_type
        fields="__all__"

class Property_listing_typeViewSerializer(serializers.ModelSerializer):
    # user=AgentLicSerializer()
    class Meta:
        model=Property_Listing_Type
        fields="__all__"

class PropertyTypeFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model=Property_Type
        fields="__all__"


class SeenPropertylistingSerializer(serializers.ModelSerializer):
    class Meta:
        modals=Seen_Property_listing
        field="__all__"

class PropertyListUserPropfile(serializers.ModelSerializer):
    user_profile=AgentProfileSerializer()
    property_city=CitySerializer()
    property_state=StateSerializer()
    class Meta:
       model=Property_Detail   
       fields="__all__"       

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Invitation  
        fields=['id','email', 'first_name', 'last_name','license','is_accept']
    

class FilterSaveSerachSerializer(serializers.ModelSerializer):
    class Meta:
        model = filter_save_serach
        fields= "__all__"

class FilterSaveSerachNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = filter_save_serach
        fields= "__all__"

class HomeCardTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeCardTitle
        fields= "__all__"

class HomeCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeCard
        fields= "__all__"      

class Property_listing_event_ViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property_listing_event
        fields = "__all__"

class PropertyAmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Property_Amenities
        fields="__all__"

class PetPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = PetProperty
        fields = ["pet_master"]

class Property30minshow_property_Serailizer(serializers.ModelSerializer):
    class Meta:
        model = Property30minshow
        fields = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

class Property_Space_Availability_Property_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Property_Space_Availability
        fields = ["space","size","term","rate","type"]

class OpenHousePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenHouseProperty
        fields = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

class GetPropertyDetailSerializer(serializers.ModelSerializer):
    user_profile=AgentProfileSerializer()
    property_city=CitySerializer()
    property_state=StateSerializer()
    property_area = AreaMasterSerializer()
    property_main_category = PropertyMainCategorySerializer()
    propertylisting_type = Property_listing_typeViewSerializer()
    property_listing_type = Propertylisting_typeViewSerializer()
    property_listing_event = serializers.SerializerMethodField()
    property_amenities = serializers.SerializerMethodField()
    property_pet = serializers.SerializerMethodField()
    property_30_min = serializers.SerializerMethodField()
    property_teammember = serializers.SerializerMethodField()
    property_space = serializers.SerializerMethodField()
    open_house_property = serializers.SerializerMethodField()

    class Meta:
        model=Property_Detail
        fields="__all__"

    def get_property_listing_event(self, obj):
        event = Property_listing_event.objects.get(property_details=obj)
        event_serializer = Property_listing_event_ViewSerializer(event)
        return event_serializer.data

    def get_property_amenities(self, obj):
        id=[]
        amenities = Property_Amenities.objects.filter(property_details=obj)
        for i in amenities:
            id.append(i.amenites_master.id)
        return id
    
    def get_property_pet(self, obj):
        pet_master_id=[]
        petobj = PetProperty.objects.filter(property_details=obj)
        for i in petobj:
            pet_master_id.append(i.pet_master.id)
        return pet_master_id
    
    def get_property_30_min(self, obj):
        property30min = Property30minshow.objects.filter(property_details=obj).last()
        event_serializer1 = Property30minshow_property_Serailizer(property30min)
        return event_serializer1.data

    def get_property_teammember(self, obj):
        teamid = []
        teamobj = TeamProperty.objects.filter(propertydetail_id = obj)
        for i in teamobj:
            teamid.append(i.userprofile_id.id)
        return teamid

    def get_property_space(self, obj):
        spaceobj = Property_Space_Availability.objects.filter(Property = obj)
        event_serializer2 = Property_Space_Availability_Property_Serializer(spaceobj, many = True)
        return event_serializer2.data

    def get_open_house_property(self, obj):
        openhouseobj = OpenHouseProperty.objects.filter(property_details = obj).last()
        openhouseserializer = OpenHousePropertySerializer(openhouseobj)
        return openhouseserializer.data
class AgentPropertySerializer(serializers.ModelSerializer):
    guest_users_save_listing = serializers.SerializerMethodField()
    class Meta:
        model=Property_Detail
        fields = "__all__"
    def get_guest_users_save_listing(self, obj):
        try:
            user = User.objects.get(id = self.context["user_id"].id)
            if Guest_Users_Save_Listing.objects.filter(user=user).filter(property_details  = obj).last():
                return True
            else:
                return False
        except Exception as e:
            return False
class PropertyDetailSerializer(serializers.ModelSerializer):
    user_profile=AgentProfileSerializer()
    property_city=CitySerializer()
    property_state=StateSerializer()
    property_area = AreaMasterSerializer()
    property_main_category = PropertyMainCategorySerializer()
    propertylisting_type = Property_listing_typeViewSerializer()
    property_listing_type = Propertylisting_typeViewSerializer()
    property_listing_event = serializers.SerializerMethodField()
    note = serializers.SerializerMethodField()
    amenity_list = serializers.SerializerMethodField()
    class Meta:
        model=Property_Detail
        fields="__all__"
    
    def get_property_listing_event(self, obj):
        event = Property_listing_event.objects.filter(property_details=obj).last()
        event_serializer = Property_listing_event_ViewSerializer(event)
        return event_serializer.data
    def get_note(self, obj):
        try:
            virtual_id = self.context['virtual_office_id']
            user = self.context['user']
            noteobj = VirtualOfficeProperty.objects.filter(Q(propertyid = obj),Q(user=user)).get(virtualofficeid = virtual_id)
            note = noteobj.note
            return note
        except Exception as e:
            return ''
    def get_amenity_list(self, obj):
        try:
            amenity_list = Property_Amenities.objects.filter(property_details = obj)
            serializer = PropertyamenitiesSeriallizer(amenity_list, many=True)
            return serializer.data
        except Exception as e:
            return ''
        
class TeamPropertySerializer(serializers.ModelSerializer):
    propertydetail_id = PropertyDetailSerializer()
    class Meta:
        model = TeamProperty
        fields= "__all__"


class Property_listing_event_Serializer(serializers.ModelSerializer):
    property_details = PropertyDetailSerializer()
    class Meta:
        model = Property_listing_event
        fields = "__all__"

class GuestUsersSaveListingSerializerforDesktop(serializers.ModelSerializer):
    class Meta:
        model = Guest_Users_Save_Listing
        fields = ['id','property_details']

class Seen_Property_listingSerializerforuser(serializers.ModelSerializer):
    class Meta:
        model = Seen_Property_listing
        fields = ['id','user_profile_id']

class GuestUsersSaveListingSerializerforuser(serializers.ModelSerializer):
    class Meta:
        model = Guest_Users_Save_Listing
        fields = ['id','is_property_available','notes','rating']

class PropertySerializer(serializers.ModelSerializer):
    property_city=CitySerializer()
    property_state=StateSerializer()
    property_area = AreaMasterSerializer()
    property_main_category = PropertyMainCategorySerializer()
    property_sub_category = PropertySubCategorySerializer()
    propertylisting_type = Property_listing_typeViewSerializer()
    property_listing_type = Propertylisting_typeViewSerializer()
    user_profile = UserProfileTemaleaderSerializer()
    guest_users_save_listing = serializers.SerializerMethodField()
    seen_property_listing = serializers.SerializerMethodField()
    open_house_property = serializers.SerializerMethodField()
    property_30_min = serializers.SerializerMethodField()
    amenity_list = serializers.SerializerMethodField()
    class Meta:
        model = Property_Detail
        fields = ['id','slug','Apt','property_title',
                'propert_description','property_listing_type', 
                'propertylisting_type', 
                'property_main_image', 
                'property_main_category',
                'property_sub_category',
                'property_type',
                'property_address_1',
                'property_address_2',
                'property_zip',
                'property_terms',
                'fees',
                'SellerAgency',
                'BuyerAgency',
                'property_offer',
                'property_area',
                'property_city',
                'property_state',
                'min_30_shows',
                'is_property_open',
                'is_property_expired',
                'is_property_exclusive',
                'property_listing_amount',
                'Square_sqft',
                'user_profile',
                'Bedrooms',
                'Bathrooms',
                'Square_sqft',
                'Exterior_Sqft',
                'Maintence_fee',
                'Real_Estate_Tax',
                'Financing',
                'Minimum_Down',
                'Units',
                'Rooms',
                'Block',
                'Lot',
                'Zone',
                'Building_Sqft',
                'Lot_Dimensions',
                'Building_Dimension',
                'Stories',
                'FAR',
                'Assessment',
                'Annual_Taxes',
                'Available_Air_Rights',
                'latitude','longitude',
                'property_main_floor_plan',
                'guest_users_save_listing',
                'seen_property_listing','open_house','open_house_property','property_30_min',
                'amenity_list']
    
    def get_guest_users_save_listing(self, obj):
        # retrieve the related Guest_Users_Save_Listing data for the current user
        user = self.context['user_id']
        guest_users_save_listing_qs = Guest_Users_Save_Listing.objects.filter(property_details=obj,user=user)
        is_save = guest_users_save_listing_qs.exists()
        # is_save = guest_users_save_listing_qs.exists()
        # serialize the retrieved data using the GuestUsersSaveListingSerializer
        # return GuestUsersSaveListingSerializerforuser(guest_users_save_listing_qs, many=True).data
        return is_save

    def get_seen_property_listing(self, obj):
        # retrieve the related Guest_Users_Save_Listing data for the current user
        user = self.context['user_id']
        seen_property_listing_qs = Seen_Property_listing.objects.filter(property_detail_id=obj,user_profile_id=user)
        is_seen = seen_property_listing_qs.exists()
        # serialize the retrieved data using the GuestUsersSaveListingSerializer
        # return Seen_Property_listingSerializerforuser(seen_property_listing_qs, many=True).data
        return is_seen
    
    def get_open_house_property(self, obj):
        openhouseobj = OpenHouseProperty.objects.filter(property_details = obj).last()
        openhouseserializer = OpenHousePropertySerializer(openhouseobj)
        return openhouseserializer.data
    
    def get_property_30_min(self, obj):
        property30min = Property30minshow.objects.filter(property_details=obj).last()
        event_serializer1 = Property30minshow_property_Serailizer(property30min)
        return event_serializer1.data
    def get_amenity_list(self, obj):
        try:
            amenity_list = Property_Amenities.objects.filter(property_details = obj)
            serializer = PropertyamenitiesSeriallizer(amenity_list, many=True)
            return serializer.data
        except Exception as e:
            return ''

class Amenities_Details(serializers.ModelSerializer):
    class Meta:
        model = Amenities_Master
        fields = ['amenities_name']

class PropertyamenitiesSeriallizer(serializers.ModelSerializer):
    amenites_master = Amenities_Details()
    class Meta:
        model = Property_Amenities
        fields = ['id', 'amenites_master', 'amenities_value', 'property_details']

class PropertySpaceAvaliableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property_Space_Availability
        fields = '__all__'

class NeighborAvaliableProfileSerializer(serializers.ModelSerializer):
    user_type = UsertypeTypeserializer()
    class Meta:
        model = UserProfile
        fields = ['id',"first_name","last_name","profile_image","user_type"]

class Get30minSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Property30minshow
        fields = '__all__'

class GuestUsersSaveListingSerializer(serializers.ModelSerializer):
    property_details = PropertyDetailSerializer()
    class Meta:
        model = Guest_Users_Save_Listing
        fields = "__all__"

class UserProfileImageWithNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','profile_image','first_name','last_name']


class ReviewSerializer(serializers.ModelSerializer):
    AgentUser = UserProfileImageWithNameSerializer()
    class Meta:
        model = Review
        fields = ['id','AgentUser','user','meet','Recommend','experience','created_date']


class GetTermsSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Terms
        fields = '__all__'

class GetOfferSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'

class ListingSlugSerializers(serializers.ModelSerializer):
    class Meta:
        model = Property_Detail
        fields = ['id','slug']