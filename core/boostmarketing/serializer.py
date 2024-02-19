from rest_framework import serializers
from .models import *

class BoostMarkitingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model=BoostMarkitingPlan
        fields="__all__"

class BoostMarkitingTableSerializer(serializers.ModelSerializer):
    class Meta:
        model=BoostMarketingTable
        fields="__all__"

class BoostMarkitingPlanTermsandServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Plan_Type
        fields=['termsandservices']