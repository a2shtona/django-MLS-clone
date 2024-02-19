from dataclasses import field
from rest_framework import serializers


from .models import *
from property.models import *
from master.serializer import *


# # AdminCustomSerializer
# class AdminCustomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = "__all__"

# Registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    # pasword2 = serializers.CharField(style={"input_type":"password"},write_only=True)
    
    class Meta:
        model = User
        fields =["password","last_login","username","is_superuser","is_staff","is_active","date_joined",
        "email","is_email_verified"]
        extra_kwargs ={
            'pasword': {'write_only':True}
        }


    def create(self,validate_data):
        return User.objects.create_user(**validate_data)


# Login
class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:  
        model=User
        fields ="__all__"


# Profile
class UserProfileSerializer(serializers.ModelSerializer):
    state=StateSerializer()
    # zip_code=ZipcodeSerializer()
    class Meta:
        model = UserProfile
        fields = "__all__"


# Change Password
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=10, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=10, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password does not match")
        user.set_password(password)
        user.save()
        return attrs

class ChangeProfileImage(serializers.Serializer):
    image_url = serializers.ImageField(required=False)
    class Meta:
        model = UserProfile
        fields = ['id','user_type' 'profile_image']

    
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']

class AccountSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountSetting
        fields = "__all__"


class AgentProfileSerializer(serializers.ModelSerializer):
    areamaster = AreaSerializer()
    citymaster = CitySerializer()
    state = StateSerializer()
    class Meta:
        model = UserProfile
        fields = "__all__"

class AgentLicSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentLic
        fields = "__all__"

class SupportticketSerializer(serializers.ModelSerializer):
    class Meta:
        model= SupportTickets
        fields = "__all__"

class SubscriptionPlanServicesSerializer(serializers.ModelSerializer): 
    class Meta:
        model = SubscriptionPlanServices
        fields =["Name","monthly_price","yearly_price"]

class AgentApprovedSubscriptionPlanserializer(serializers.ModelSerializer):
    plan_id = SubscriptionPlanServicesSerializer()
    class Meta:
        model= AgentApprovedSubscriptionPlan
        fields = "__all__" 

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ["id","card_name","card_number","month","year"]

class BillingSerializer(serializers.ModelSerializer):
    card_id=CardSerializer()
    cityid=CitySerializer()
    stateid=StateSerializer()
    # zipcodeid=ZipcodeSerializer()
    class Meta:
        model = Billing
        fields= "__all__"


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = "__all__"

class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["profile_image"]

class NeighborhoodSpecilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Nb_specality_area
        fields ="__all__"

class min_30_Serializer(serializers.ModelSerializer):
    class Meta:
        model = min_30
        fields = "__all__"

class NeighborhoodSpecilityAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nb_specality_area
        fields =["id","area_id","doc1","doc2","doc3"]


class UserProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','profile_image']

class UsertypeTypeserializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user_type']

class UserProfileTemaleaderSerializer(serializers.ModelSerializer):
    state=StateSerializer()
    user_type = UsertypeTypeserializer()
    class Meta:
        model = UserProfile
        fields = "__all__"

class UserProfileImageNameSerializer(serializers.ModelSerializer):
    language_name = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = ['profile_image','first_name','last_name','address_line_1','rating','language_name']
    
    def get_language_name(self, obj):
        if obj.languages:
            language = LanguageMaster.objects.filter(id__in = obj.languages)
            language_obj = loadLanguageSerializer(language, many=True).data
        else:
            language_obj = None
        return language_obj

class GetIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueType
        fields = "__all__"

class GetPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = IssuePriority
        fields = "__all__"

class SalesPersonSearchSerializer(serializers.ModelSerializer):
    saved = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = ['id', 'slug', 'profile_image', 'rating', 'first_name', 'last_name', 'saved']
    
    def get_saved(self, obj):
        user = self.context['user']
        if SavedSalesPerosn.objects.filter(userprofile = obj, user = user):
            save = True
        else:
            save = False
        return save