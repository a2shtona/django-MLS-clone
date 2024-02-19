from rest_framework import serializers
from .models import *
from accounts.serializers import AgentProfileSerializer
from master.serializer import *
from accounts.serializers import *
from property.serializer import *
from django.db.models import Q
class VirtualOfficeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualOffice
        fields=["id","userprofile",'virtual_office_name']


class PropertyVitualAgentSerializer(serializers.ModelSerializer):
    property_city=CitySerializer()
    property_state=StateSerializer()
    property_area = AreaMasterSerializer()
    property_main_category = PropertyMainCategorySerializer()
    property_sub_category = PropertySubCategorySerializer()
    propertylisting_type = Property_listing_typeViewSerializer()
    property_listing_type = Propertylisting_typeViewSerializer()
    user_profile = UserProfileTemaleaderSerializer()
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
                'property_main_floor_plan','open_house']

class Custom_Info_Id_Serializer(serializers.ModelSerializer):
    virtual_office_count = serializers.SerializerMethodField()
    virtual_office_name = serializers.SerializerMethodField()
    class Meta:
        model = customer_info
        fields = ["id", "name", "current_address","contact_no_1","virtual_office_count","virtual_office_name"]
    
    def get_virtual_office_count(self, obj):
        if User.objects.filter(email = obj.user.email):
            user_obj = User.objects.get(email = obj.user.email)
            virtual_office_count = VirtualOfficeTeam.objects.filter(email = user_obj.email).count()
        else:
            virtual_office_count = None
        return virtual_office_count

    def get_virtual_office_name(self, obj):
        if User.objects.filter(email = obj.user.email):
            user_obj = User.objects.get(email = obj.user.email)
            virtual_office_count = VirtualOfficeTeam.objects.filter(email = user_obj.email).values_list('virtualid', flat=True)
            virtual_office_name = VirtualOffice.objects.filter(id__in = virtual_office_count)
            serializer = VirtualOfficeNameSerializer(virtual_office_name, many=True)
            return serializer.data
        else:
            return None

# class VirtualOfficeTeamId(serializers.ModelSerializer):
#     user_image = serializers.SerializerMethodField()
#     custom_obj = serializers.SerializerMethodField()
#     class Meta:
#         model = VirtualOfficeTeam
#         fields = ['id', 'user_image', 'custom_obj']

#     def get_user_image(self, obj):
#         try:
#             user = User.objects.filter(email=obj.email)
#             usertype = UserType.objects.filter(user__in=user)
#             userprofile = UserProfile.objects.filter(user_type__in = usertype).last()
#             userprofileobj = UserProfileImageSerializer(userprofile)
#             return userprofileobj.data
#         except User.DoesNotExist:
#             return None
    
#     def get_custom_obj(self, obj):
#         try:
#             customeobj = customer_info.objects.filter(email = obj.email).get(user = obj)
#             serializer = Custom_Info_Id_Serializer(customeobj, many=True)
#             return serializer.data
#         except User.DoesNotExist:
#             return None

# class Custom_Info_Id_Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = customer_info
#         fields = ["id", "name", "current_address"]

class VirtualOfficeTeamId(serializers.ModelSerializer):
    user_image = serializers.SerializerMethodField()
    custom_obj = serializers.SerializerMethodField()
    class Meta:
        model = VirtualOfficeTeam
        fields = ['id', 'user_image', 'custom_obj']

    def get_user_image(self, obj):
        try:
            user = User.objects.filter(email=obj.email)
            usertype = UserType.objects.filter(user__in=user)
            userprofile = UserProfile.objects.filter(user_type__in = usertype).last()
            userprofileobj = UserProfileImageSerializer(userprofile)
            return userprofileobj.data
        except User.DoesNotExist:
            return None
    
    def get_custom_obj(self, obj):
        try:
            customeobj = customer_info.objects.filter(origin_email = obj.email).get(user = obj)
            serializer = Custom_Info_Id_Serializer(customeobj)
            return serializer.data
        except customer_info.DoesNotExist:
            return None

class Signed_Documnets_Custom_Info_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
class CustomProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = customer_info
        field = ['id', 'profile_image']
class Custom_Info_Image_Serializer(serializers.ModelSerializer):
    user_image = serializers.SerializerMethodField()
    signed_documents = serializers.SerializerMethodField()

    class Meta:
        model = customer_info
        fields = "__all__"
    def get_user_image(self, obj):
        try:
            user = User.objects.filter(email=obj.origin_email)
            usertype = UserType.objects.filter(user__in=user)
            userprofile = UserProfile.objects.filter(user_type__in = usertype).last()
            userprofileobj = UserProfileImageSerializer(userprofile)
            return userprofileobj.data
        except User.DoesNotExist:
            return None
    
    def get_signed_documents(self, obj):
        try:
            user = User.objects.get(email = obj.origin_email)
            signed_document = Document.objects.filter(user = user)
            serializer = Signed_Documnets_Custom_Info_Serializer(signed_document, many = True)
            return serializer.data
        except User.DoesNotExist:
            return None
class Custom_Info_Serializer(serializers.ModelSerializer):
    class Meta:
        model = customer_info
        fields = '__all__'

class VirtualOfficeTeamSerializer(serializers.ModelSerializer):
    user_image = serializers.SerializerMethodField()
    custom_obj = serializers.SerializerMethodField()
    class Meta:
        model = VirtualOfficeTeam
        fields = ["id","email","is_status","is_request","user_image","member_type","custom_obj"]
    
    def get_user_image(self, obj):
        try:
            user = User.objects.filter(email=obj.email)
            usertype = UserType.objects.filter(user__in=user)
            userprofile = UserProfile.objects.filter(user_type__in = usertype)
            userprofileobj = UserProfileImageSerializer(userprofile, many=True)
            return userprofileobj.data
        except User.DoesNotExist:
            return None
    
    def get_custom_obj(self, obj):
        try:
            customeobj = customer_info.objects.filter(email = obj.email)
            serializer = Custom_Info_Serializer(customeobj, many=True)
            return serializer.data
        except User.DoesNotExist:
            return None

class VirtualOfficeTeamMemberSerializer(serializers.ModelSerializer):
    user_image = serializers.SerializerMethodField()
    # custom_obj = serializers.SerializerMethodField()
    class Meta:
        model = VirtualOfficeTeam
        fields = ["id","email","is_status","is_request","user_image","member_type"]
    
    def get_user_image(self, obj):
        try:
            user = User.objects.filter(email=obj.email)
            usertype = UserType.objects.filter(user__in=user)
            userprofile = UserProfile.objects.filter(user_type__in = usertype).last()
            userprofileobj = UserProfileImageSerializer(userprofile)
            return userprofileobj.data
        except User.DoesNotExist:
            return None

class VisualProfileTeamSerializer(serializers.ModelSerializer):
    userprofile_main = serializers.SerializerMethodField()
    virtual_team = serializers.SerializerMethodField()
    class Meta:
        model = VirtualOffice
        fields=["id","userprofile_main",
                'virtual_office_name',
                "slug",
                "virtual_team"
                ]
    
    def get_userprofile_main(self, obj):
        try:
            virtual_office_main_user = VirtualOfficeTeam.objects.filter(virtualid=obj).get(member_type = "Main")
            event_serializer = VirtualOfficeTeamMemberSerializer(virtual_office_main_user)
            return event_serializer.data
        except VirtualOfficeTeam.DoesNotExist:
            return None

    def get_virtual_team(self, obj):
        try:
            event = VirtualOfficeTeam.objects.filter(virtualid=obj).filter(member_type = "Other")
            event_serializer = VirtualOfficeTeamMemberSerializer(event, many=True)
            return event_serializer.data
        except VirtualOfficeTeam.DoesNotExist:
            return None


class AgentProfileVirtualOfficeSerializer(serializers.ModelSerializer):
    userprofile = UserProfileImageNameSerializer()
    class Meta:
        model = VirtualOffice
        fields=["id","userprofile",
                'virtual_office_name',
                "slug",]

class VirtualofficeUserProfileImageNameSerializer(serializers.ModelSerializer):
    user_type = UsertypeTypeserializer()
    class Meta:
        model = UserProfile
        fields="__all__"


class VirtualOffice_Like_Dislike_Note_Serializer(serializers.ModelSerializer):
    userprofile = serializers.SerializerMethodField()    
    propertyid = PropertyVitualAgentSerializer()
    class Meta:
        model = VirtualOfficeProperty
        fields="__all__"
    
    def get_userprofile(self, obj):
        userobj = User.objects.get(id = obj.user.id)
        user_tyep_obj = UserType.objects.get(user = userobj)
        userprofileobj = UserProfile.objects.get(user_type = user_tyep_obj)
        serializer = VirtualofficeUserProfileImageNameSerializer(userprofileobj).data
        return serializer


        
class PropertyDetailvirtualSerializer(serializers.ModelSerializer):
    user_profile=AgentProfileSerializer()
    property_city=CitySerializer()
    property_state=StateSerializer()
    property_area = AreaMasterSerializer()
    property_main_category = PropertyMainCategorySerializer()
    propertylisting_type = Property_listing_typeViewSerializer()
    property_listing_type = Propertylisting_typeViewSerializer()
    property_listing_event = serializers.SerializerMethodField()
    likedislike = serializers.SerializerMethodField()
    note = serializers.SerializerMethodField()
    amenity_list = serializers.SerializerMethodField()
    class Meta:
        model=Property_Detail
        fields="__all__"
    
    def get_property_listing_event(self, obj):

        event = Property_listing_event.objects.filter(property_details=obj).last()
        event_serializer = Property_listing_event_ViewSerializer(event)
        return event_serializer.data

    def get_likedislike(self, obj):
        user = self.context['virtual_id']
        userobj = self.context['userid']

        try:
            noteobj = VirtualOfficeProperty.objects.filter(Q(propertyid = obj),Q(user=userobj)).get(virtualofficeid = user)
            if noteobj.is_like:
                ret = True
            else:
                ret = False
            return ret
        except Exception as e:
            return -1

    def get_note(self, obj):
        user = self.context['virtual_id']
        userobj = self.context['userid']

        try:
            noteobj = VirtualOfficeProperty.objects.filter(Q(propertyid = obj),Q(user=userobj)).get(virtualofficeid = user)
            noteid = noteobj.note
            return noteid
        except Exception as e:
            return ''
    def get_amenity_list(self, obj):
        try:
            amenity_list = Property_Amenities.objects.filter(property_details = obj)
            serializer = PropertyamenitiesSeriallizer(amenity_list, many=True)
            return serializer.data
        except Exception as e:
            return ''
# class VirtualOffice_Agent_Like_Dislike_Note_Serializer(serializers.ModelSerializer):
#     propertyid = PropertyVitualAgentSerializer()
#     class Meta:
#         model = NoteOnVirtualOfficeProperty
#         fields = ['id','propertyid','note','is_like','is_dislike']

class ReviewUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','profile_image','first_name','last_name','rating']

class AgnetTeamPropertySerializer(serializers.ModelSerializer):
    propertydetail_id = PropertyDetailvirtualSerializer()
    class Meta:
        model = TeamProperty
        fields= "__all__"

class PropertyDetailIdvirtualSerializer(serializers.ModelSerializer):
    user_profile=AgentProfileSerializer()
    property_city=CitySerializer()
    property_state=StateSerializer()
    property_area = AreaMasterSerializer()
    property_main_category = PropertyMainCategorySerializer()
    propertylisting_type = Property_listing_typeViewSerializer()
    property_listing_type = Propertylisting_typeViewSerializer()
    property_listing_event = serializers.SerializerMethodField()
    # likedislike = serializers.SerializerMethodField()
    class Meta:
        model=Property_Detail
        fields="__all__"
    
    def get_property_listing_event(self, obj):
        event = Property_listing_event.objects.filter(property_details=obj).last()
        event_serializer = Property_listing_event_ViewSerializer(event)
        return event_serializer.data

# class ShowPropertySerailizer(serializers.ModelSerializer):
#     propertyid = PropertyDetailIdvirtualSerializer()
#     note = serializers.SerializerMethodField()
#     class Meta:
#         model = VirtualOfficeProperty
#         fields = ['id','propertyid','note']
    
#     def get_note(self, obj):
#         noteobj = NoteOnVirtualOfficeProperty.objects.filter(virtual_office = obj.id)
#         note_id = None
#         for i in noteobj:
#             if i.note:
#                 note_id = True
#             else:
#                 note_id = False
#         return note_id

class AgentPropfileVirtualOffice(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = ['id', 'slug', 'user_type','first_name', 'last_name', 'cell_number','work_number_1','profile_image','address']
    
    def get_address(self, obj):
        user_profile_obj = UserProfile.objects.get(id = obj.id)
        return user_profile_obj.address_line_1

class GuestAgentProfileViewSerializer(serializers.ModelSerializer):
    userprofile = AgentPropfileVirtualOffice()
    class Meta:
        model = VirtualOffice
        fields = ['id', 'userprofile']

class User_Data_Custom_Serializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    current_address = serializers.SerializerMethodField()
    contact_no_1 = serializers.SerializerMethodField()
    virtual_office_count = serializers.SerializerMethodField()
    virtual_office_name = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = ["id", "name", "current_address","contact_no_1","virtual_office_count","virtual_office_name"]
    
    def get_name(self, obj):
        userprofile = UserProfile.objects.get(id = obj.id)
        if userprofile.first_name and userprofile.last_name:
            name = userprofile.first_name + " " + userprofile.last_name
        else:
            name = None
        return name

    def get_current_address(self, obj):
        userprofile = UserProfile.objects.get(id = obj.id)
        if userprofile.address_line_1:
            address = userprofile.address_line_1
        else:
            address = None
        return address
    
    def get_contact_no_1(self, obj):
        userprofile = UserProfile.objects.get(id = obj.id)
        if userprofile.cell_number:
            number = userprofile.cell_number
        else:
            number = None
        return number

    def get_virtual_office_count(self, obj):
        userprofile = UserProfile.objects.get(id = obj.id)
        user = User.objects.get(id = userprofile.user_type.user.id)
        virtual_office_count = VirtualOfficeTeam.objects.filter(email = user.email).count()
        return virtual_office_count

    def get_virtual_office_name(self, obj):
        userprofile = UserProfile.objects.get(id = obj.id)
        user = User.objects.get(id = userprofile.user_type.user.id)
        virtual_office_count = VirtualOfficeTeam.objects.filter(email = user.email).values_list('virtualid', flat=True)
        virtual_office_name = VirtualOffice.objects.filter(id__in = virtual_office_count)
        serializer = VirtualOfficeNameSerializer(virtual_office_name, many=True)
        return serializer.data

class GuestContactListSerializer(serializers.ModelSerializer):
    user_image = serializers.SerializerMethodField()
    custom_obj = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = ["id",'user_image','custom_obj']
    
    def get_user_image(self, obj):
        userprofile = UserProfile.objects.get(id = obj.id)
        userprofileobj = UserProfileImageSerializer(userprofile)
        return userprofileobj.data

    def get_custom_obj(self, obj):
        user_id = UserProfile.objects.get(id = obj.id)
        serializer = User_Data_Custom_Serializer(user_id)
        return serializer.data


class CustomInfoSerializer(serializers.ModelSerializer):
    virtual_office_count = serializers.SerializerMethodField()
    virtual_office_name = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    current_address = serializers.SerializerMethodField()
    contact_no_1 = serializers.SerializerMethodField()
    class Meta:
        model = customer_info
        fields = ["id", "name", "current_address","contact_no_1","virtual_office_count","virtual_office_name"]
    
    def get_virtual_office_count(self, obj):
        cutom_obj = customer_info.objects.filter(email__in = obj).values_list("user", flat=True).count()
        return cutom_obj
    
    def get_virtual_office_name(self, obj):
        cutom_obj = customer_info.objects.filter(email__in = obj).values_list("user", flat=True)
        vitual_team_obj = VirtualOfficeTeam.objects.filter(id__in = cutom_obj).values_list('virtualid', flat=True)
        office_obj = VirtualOffice.objects.filter(id__in = vitual_team_obj)
        serializer = VirtualOfficeNameSerializer(office_obj, many=True)
        return serializer.data

    def get_name(self, obj):
        cutom_obj = customer_info.objects.filter(email__in = obj).last()
        return cutom_obj.name
    
    def get_current_address(self, obj):
        cutom_obj = customer_info.objects.filter(email__in = obj).last()
        if cutom_obj.current_address:
            address = cutom_obj.current_address
        else:
            address = None
        return address
    
    def get_contact_no_1(self, obj):
        cutom_obj = customer_info.objects.filter(email__in = obj).last()
        return cutom_obj.contact_no_1


class VitualOfficeTeamSerializer(serializers.ModelSerializer):
    user_image = serializers.SerializerMethodField()
    custom_obj = serializers.SerializerMethodField()
    class Meta:
        model = VirtualOfficeTeam
        fields = ['id', 'user_image', 'custom_obj']
    
    def get_user_image(self, obj):
        try:
            user = User.objects.filter(email=obj)
            usertype = UserType.objects.filter(user__in=user)
            userprofile = UserProfile.objects.filter(user_type__in = usertype).last()
            userprofileobj = UserProfileImageSerializer(userprofile)
            return userprofileobj.data
        except User.DoesNotExist:
            return None
    
    def get_custom_obj(self, obj):
        customeobj = customer_info.objects.filter(email = obj).values_list('email', flat=True).distinct()
        serializer = CustomInfoSerializer(customeobj)
        return serializer.data
class CustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']
class DocumentSerializers(serializers.ModelSerializer):
    userprofile = serializers.SerializerMethodField()
    class Meta:
        model = Document
        fields = "__all__"
    def get_userprofile(self, obj):
        try:
            user = User.objects.get(email=obj.user)
            usertype = UserType.objects.get(user=user)
            userprofile = UserProfile.objects.get(user_type = usertype)
            response = {
                "email": user.email,
                "first_name": userprofile.first_name,
                "last_name": userprofile.last_name
            }
            return response
        except User.DoesNotExist:
            return None
class ShareDocumentSerializers(serializers.ModelSerializer):
    agentprofile = serializers.SerializerMethodField()
    signed_document = serializers.SerializerMethodField()
    class Meta:
        model = Document
        fields = ["id", "agentprofile", "file", "filename", "created_at", "updated_at", "signed_document"]
    def get_agentprofile(self, obj):
        try:
            user = User.objects.get(email=obj.share_from)
            usertype = UserType.objects.get(user=user)
            userprofile = UserProfile.objects.get(user_type = usertype)
            response = {
                "email": user.email,
                "first_name": userprofile.first_name,
                "last_name": userprofile.last_name
            }
            return response
        except User.DoesNotExist:
            return None
    def get_signed_document(self, obj):
        try:
            user_id = self.context['user_id']
            user = User.objects.get(id = user_id)
            signed_document = Document.objects.filter(user = user, signing = obj.id, signed = True).last()
            serializer = DocumentSerializers(signed_document)
            return serializer.data
        except Document.DoesNotExist:
            return None
class SinginedDocumentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Signed_Documnets_Custom_Info
        fields = "__all__"

class AgentDetailSerializer(serializers.ModelSerializer):
    current_list = serializers.SerializerMethodField()
    close_list = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = "__all__"
    def get_current_list(self, obj):
        if Property_Detail.objects.filter(user_profile = self.context["userprofile"], is_property_open=True):
            current_list = Property_Detail.objects.filter(user_profile = self.context["userprofile"], is_property_open=True)
            serializer=AgentPropertySerializer(current_list, many=True)
            return serializer.data
    def get_close_list(self, obj):
        if Property_Detail.objects.filter(user_profile = self.context["userprofile"], is_property_open=False):
            close_list = Property_Detail.objects.filter(user_profile = self.context["userprofile"], is_property_open=False)
            serializer=AgentPropertySerializer(close_list, many=True)
            return serializer.data
