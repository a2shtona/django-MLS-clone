from rest_framework import serializers
from .models import *




class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model=CountryMaster
        fields="__all__"

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model=StateMaster   
        fields="__all__"

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model=CityMaster   
        fields="__all__"
    
class ZipcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model=ZipCodeMaster   
        fields=['Zipcode','id']

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model=AreaMaster   
        fields="__all__"    


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model=PetMaster   
        fields="__all__"  

class loadLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model=LanguageMaster
        fields="__all__"

class CountrySearchSerializer(serializers.ModelSerializer):
    class Meta:
        model=CountryMaster
        fields="__all__"

class StateSearchSerializer(serializers.ModelSerializer):
    country_master=CountrySearchSerializer()
    class Meta:
        model=StateMaster   
        fields="__all__"

class CitySearchSerializer(serializers.ModelSerializer):
    state_master=StateSearchSerializer()
    class Meta:
        model=CityMaster   
        fields="__all__"

class AreaSearchSerializer(serializers.ModelSerializer):
        city_master=CitySearchSerializer()
        class Meta:
            model=AreaMaster
            fields="__all__"

class ZipcodeSearchSerializer(serializers.ModelSerializer):
        area_master=AreaSearchSerializer()
        class Meta:
            model=ZipCodeMaster
            fields="__all__"     

class ServiceSerializer(serializers.ModelSerializer):
        class Meta:
            model=SubscriptionServices
            fields="__all__"

class SubscriptionplanSerializer(serializers.ModelSerializer):
    
    class Meta:
            model=SubscriptionPlanServices      
            fields="__all__" 


class AreaMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=AreaMaster
        fields="__all__"

class citymasterSerializer(serializers.ModelSerializer):
    area=AreaMasterSerializer(many=True,source='areamaster_set')
    class Meta:
        model=CityMaster
        fields="__all__"

