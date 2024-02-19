from property.models import *
from .models import *
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate,login ,logout
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.models import *
from accounts.serializers import *
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from accounts.utils import Util
from django.contrib import messages
from .resource import *
from tablib import Dataset
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.views import APIView
from .serializer import *
from rest_framework.response import *
from django.utils.decorators import method_decorator
from master import util
from rest_framework.permissions import IsAuthenticated
import datetime 
from .adminapiserializers import *
from accounts.paginatorviews import *
from advertisement.models import *
from advertisement.serializer import *
from property.serializer import *

def getuseprofile(request, search, usertype):
    if search is not None:
        multiple_q = Q(Q(first_name__icontains = search) | Q(last_name__icontains = search))
        userprofile=UserProfile.objects.filter(user_type__in = usertype).filter(multiple_q)

class AllTypeUser(APIView):
    def get(self, request, format = None):
        user = User.objects.all().exclude(is_superuser = True)
        usertype = UserType.objects.filter(user__in = user).values_list("id", flat=True)
        search = request.GET.get('search')
        if search:
            multiple_q = Q(Q(first_name__icontains = search) | Q(last_name__icontains = search))
            userprofile=UserProfile.objects.filter(user_type_id__in=usertype).filter(multiple_q)
        else:
            userprofile=UserProfile.objects.filter(user_type_id__in=usertype)
        serializer = UserProfileListingSerializer(userprofile, many = True)
        return Response(util.success(self,serializer.data))

class GuestTypeUser(APIView):
    def get(self, request, format = None):
        usertype = UserType.objects.filter(user_type=1).values_list("id", flat=True)
        search = request.GET.get('search')
        if search:
            multiple_q = Q(Q(first_name__icontains = search) | Q(last_name__icontains = search))
            userprofile=UserProfile.objects.filter(user_type_id__in=usertype).filter(multiple_q)
        else:
            userprofile=UserProfile.objects.filter(user_type_id__in=usertype)
        serializer = UserProfileListingSerializer(userprofile, many = True)
        return Response(util.success(self,serializer.data))

class AgentTypeUser(APIView):
    def get(self, request, format=None):
        usertype = UserType.objects.filter(user_type = 2).values_list("id", flat=True)
        search = request.GET.get('search')
        if search:
            multiple_q = Q(Q(first_name__icontains = search) | Q(last_name__icontains = search))
            userprofile=UserProfile.objects.filter(user_type_id__in=usertype).filter(multiple_q)
        else:
            userprofile=UserProfile.objects.filter(user_type_id__in=usertype)
        serializer = UserProfileListingSerializer(userprofile, many = True)
        return Response(util.success(self,serializer.data))

class InvestorAndDeveloperUser(APIView):
    def get(self, request, format = None):
        usertype = UserType.objects.filter(user_type = 3).values_list("id", flat=True)
        search = request.GET.get('search')
        if search:
            multiple_q = Q(Q(first_name__icontains = search) | Q(last_name__icontains = search))
            userprofile=UserProfile.objects.filter(user_type_id__in=usertype).filter(multiple_q)
        else:
            userprofile=UserProfile.objects.filter(user_type_id__in=usertype)
        serializer = UserProfileListingSerializer(userprofile, many = True)
        return Response(util.success(self,serializer.data))
    
class FsbhoAndFrbhoUser(APIView):
    def get(self, request, format = None):
        usertype = UserType.objects.filter(user_type = 4).values_list("id", flat=True)
        search = request.GET.get('search')
        if search:
            multiple_q = Q(Q(first_name__icontains = search) | Q(last_name__icontains = search))
            userprofile=UserProfile.objects.filter(user_type_id__in=usertype).filter(multiple_q)
        else:
            userprofile=UserProfile.objects.filter(user_type_id__in=usertype)
        serializer = UserProfileListingSerializer(userprofile, many = True)
        return Response(util.success(self,serializer.data))

class ManagementUser(APIView):
    def get(self, request, format = None):
        usertype = UserType.objects.filter(user_type = 5).values_list("id", flat=True)
        search = request.GET.get('search')
        if search:
            multiple_q = Q(Q(first_name__icontains = search) | Q(last_name__icontains = search))
            userprofile=UserProfile.objects.filter(user_type_id__in=usertype).filter(multiple_q)
        else:
            userprofile=UserProfile.objects.filter(user_type_id__in=usertype)
        serializer = UserProfileListingSerializer(userprofile, many = True)
        return Response(util.success(self,serializer.data))

class SubAgentUser(APIView):
    def get(self, request, format = None):
        usertype = UserType.objects.filter(user_type = 6).values_list("id", flat=True)
        search = request.GET.get('search')
        if search:
            multiple_q = Q(Q(first_name__icontains = search) | Q(last_name__icontains = search))
            userprofile=UserProfile.objects.filter(user_type_id__in=usertype).filter(multiple_q)
        else:
            userprofile=UserProfile.objects.filter(user_type_id__in=usertype)
        serializer = UserProfileListingSerializer(userprofile, many = True)
        return Response(util.success(self,serializer.data))

class BoostMarketingUser(APIView):
    def get(self, request, format = None):
        usertype = UserType.objects.filter(user_type = 7).values_list("id", flat=True)
        search = request.GET.get('search')
        if search:
            multiple_q = Q(Q(first_name__icontains = search) | Q(last_name__icontains = search))
            userprofile=UserProfile.objects.filter(user_type_id__in=usertype).filter(multiple_q)
        else:
            userprofile=UserProfile.objects.filter(user_type_id__in=usertype)
        serializer = UserProfileListingSerializer(userprofile, many = True)
        return Response(util.success(self,serializer.data))

class AdvertisementUserList(APIView):
    def get(self, request, format = None):
        search = request.GET.get('search')
        adevertisementuser = AdvertismentUser.objects.all()
        serializer = AdvertismentRegistrationSerializer(adevertisementuser, many=True)
        return Response(util.success(self,serializer.data))

class InactiveUserList(APIView):
    def get(self, request, format = None):
        userobj = User.objects.filter(is_active=False)
        usertype = UserType.objects.filter(user__in = userobj).values_list("id", flat=True)
        search = request.GET.get('search')
        if search:
            multiple_q = Q(Q(first_name__icontains = search) | Q(last_name__icontains = search))
            userprofile=UserProfile.objects.filter(user_type_id__in=usertype).filter(multiple_q)
        else:
            userprofile=UserProfile.objects.filter(user_type_id__in=usertype)
        serializer = UserProfileListingSerializer(userprofile, many = True)
        return Response(util.success(self,serializer.data))

class CountryAdminAPI(APIView):
    def get(self, request, format = None):
        search = request.GET.get('search')
        if search:
            multiple_q = Q(Q(country_name__icontains = search) | Q(country_code__icontains = search))
            countryobj = CountryMaster.objects.filter(multiple_q)
        else:
            countryobj = CountryMaster.objects.all()
        serializer = CountrySearchSerializer(countryobj, many=True)
        return Response(util.success(self, serializer.data))

class StateAdminAPI(APIView):
    def get(self, request, format = None):
        search = request.GET.get('search')
        if search:
            multiple_q = Q(state_name__icontains = search)
            stateobj = StateMaster.objects.filter(multiple_q)
        else:
            stateobj = StateMaster.objects.all()
        serializer = StateSearchSerializer(stateobj, many=True)
        return Response(util.success(self, serializer.data))

class CityAdminAPI(APIView):
    def get(self, request, format = None):
        search = request.GET.get('search')
        if search:
            multiple_q = Q(city_name__icontains = search)
            cityobj = CityMaster.objects.filter(multiple_q)
        else:
            cityobj = CityMaster.objects.all()
        serializer = CitySearchSerializer(cityobj, many=True)
        return Response(util.success(self, serializer.data))

class AreaAdminAPI(APIView):
    def get(self, request, format = None):
        search = request.GET.get('search')
        if search:
            multiple_q = Q(area_name__icontains = search)
            areaobj = AreaMaster.objects.filter(multiple_q)
        else:
            areaobj = AreaMaster.objects.all()
        serializer = AreaSearchSerializer(areaobj, many=True)
        return Response(util.success(self, serializer.data))

class ZipCodeAdminAPI(APIView):
    def get(self, request, format = None):
        search = request.GET.get('search')
        if search:
            multiple_q = Q(Zipcode__icontains = search)
            zopobj = ZipCodeMaster.objects.filter(multiple_q)
        else:
            zopobj = ZipCodeMaster.objects.all()
        serializer = ZipcodeSearchSerializer(zopobj, many=True)
        return Response(util.success(self, serializer.data))

class TermsAdminAPI(APIView):
    def get(self, request, format = None):
        search = request.GET.get('search')
        if search:
            multiple_q = Q(terms__icontains = search)
            termobj = Terms.objects.filter(multiple_q)
        else:
            termobj = Terms.objects.all()
        serializer = GetAdminTermsSerilizer(termobj, many=True)
        return Response(util.success(self, serializer.data))

class AllPendingLicenceAdminAPI(APIView):
    def get(self, request, format = None):
        search = request.GET.get('search')
        if search:
            multiple_q = Q(license_number__icontains = search)
            licobj = AgentLic.objects.filter(multiple_q).filter(is_validated = False, is_requested = True)[::-1]
        else:
            licobj = AgentLic.objects.filter(is_validated = False, is_requested = True)[::-1]
        serializer = AgentLicAdminSerializer(licobj, many=True)
        return Response(util.success(self, serializer.data))

class AllNBSpecilityAdminAPI(APIView):
    def get(self, request, format = None):
        search = request.GET.get('search')
        if search:
            Neighboorhoodobj = Nb_specality_area.objects.filter(is_verified="Pending")
        else:
            Neighboorhoodobj = Nb_specality_area.objects.filter(is_verified="Pending")
        serializer = AreaNbSpecilitySerializer(Neighboorhoodobj, many=True)
        return Response(util.success(self, serializer.data))

class AllSupportTicketAdminAPI(APIView):
    def get(self, request, format = None):
        search = request.GET.get('search')
        if search:
            multiple_q = Q(Q(ticket_no__icontains = search) | Q(issue_type__icontains = search) | Q(title__icontains = search) | Q(description__icontains = search) | Q(priority__icontains = search))
            supportobj = SupportTickets.objects.filter(multiple_q)
        else:
            supportobj = SupportTickets.objects.all()
        serializer = SupportticketAdminSerializer(supportobj, many = True)
        return Response(util.success(self, serializer.data))

class AllAgentSupportTicketAdminAPI(APIView):
    def get(self, request, format = None):
        usertype = UserType.objects.filter(user_type = 2).values_list('user', flat=True)
        search = request.GET.get('search')
        if search:
            multiple_q = Q(Q(ticket_no__icontains = search) | Q(issue_type__icontains = search) | Q(title__icontains = search) | Q(description__icontains = search) | Q(priority__icontains = search))
            supportobj = SupportTickets.objects.filter(multiple_q).filter(user__in = usertype,ticket_no__in = search)
        else:
            supportobj = SupportTickets.objects.filter(user__in = usertype)
        serializer = SupportticketAdminSerializer(supportobj, many = True)
        return Response(util.success(self, serializer.data))

class AllGuestSupportTicketAdminAPI(APIView):
    def get(self, request, format = None):
        usertype = UserType.objects.filter(user_type = 1).values_list('user', flat=True)
        search = request.GET.get('search')
        if search:
            multiple_q = Q(Q(ticket_no__icontains = search) | Q(issue_type__icontains = search) | Q(title__icontains = search) | Q(description__icontains = search) | Q(priority__icontains = search))
            supportobj = SupportTickets.objects.filter(multiple_q).filter(user__in = usertype,ticket_no__in = search)
        else:
            supportobj = SupportTickets.objects.filter(user__in = usertype)
        serializer = SupportticketAdminSerializer(supportobj, many = True)
        return Response(util.success(self, serializer.data))

class AllLanguageAdminAPI(APIView):
    def get(self, request, fromat=None):
        search = request.GET.get('search')
        if search:
            multiple_q = Q(languages_name__icontains = search)
            languageobj = LanguageMaster.objects.filter(multiple_q)
        else:
            languageobj = LanguageMaster.objects.all()
        serializer = loadLanguageSerializer(languageobj, many = True)
        return Response(util.success(self, serializer.data))

class OfferAdminAPI(APIView):
    def get(self, request, format=None):
        search = request.GET.get('search')
        if search:
            multiple_q = Q(offer__icontains = search)
            offerobj = Offer.objects.filter(multiple_q)
        else:
            offerobj = Offer.objects.all()
        serializer = GetAdminOfferSerilizer(offerobj, many=True)
        return Response(util.success(self, serializer.data))

class HomeCardTitleAdminAPI(APIView):
    def get(self, request, format=None):
        search = request.GET.get('search')
        if search:
            multiple_q = Q(Title__icontains = search)
            homecardtitleobj = HomeCardTitle.objects.filter(multiple_q)
        else:
            homecardtitleobj = HomeCardTitle.objects.all()
        serializer = HomeCardTitleSerializer(homecardtitleobj, many=True)
        return Response(util.success(self, serializer.data))

class HomeCardAdminAPI(APIView):
    def get(self, request, format=None):
        search = request.GET.get('search')
        if search:
            multiple_q = Q(Card_Title__icontains = search)
            homecardobj = HomeCard.objects.filter(multiple_q)
        else:
            homecardobj = HomeCard.objects.all()
        serializer = HomeCardSerializer(homecardobj, many=True)
        return Response(util.success(self, serializer.data))

class PropertyListingAdminAPI(APIView):
    def get(self, request, format=None):
        search = request.GET.get('search')
        if search:
            multiple_q = Q(property_listing_name__icontains = search)
            listingobj = Propertylisting_type.objects.filter(multiple_q)
        else:
            listingobj = Propertylisting_type.objects.all()
        serializer = Propertylisting_typeViewSerializer(listingobj, many=True)
        return Response(util.success(self, serializer.data))

class PropertyTypeListingAdminAPI(APIView):
    def get(self, request, format=None):
        search = request.GET.get('search')
        if search:
            multiple_q = Q(listing_type__icontains = search)
            listingobj = Property_Listing_Type.objects.filter(multiple_q)
        else:
            listingobj = Property_Listing_Type.objects.all()
        serializer = Property_listing_typeViewAdminSerializer(listingobj, many=True)
        return Response(util.success(self, serializer.data))

class MainCategoryAdminAPI(APIView):
    def get(self, request, format=None):
        search = request.GET.get('search')
        if search:
            multiple_q = Q(Main_category__icontains = search)
            listingobj = Property_Main_Category.objects.filter(multiple_q)
        else:
            listingobj = Property_Main_Category.objects.all()
        serializer = PropertyMainAdminCategorySerializer(listingobj, many=True)
        return Response(util.success(self, serializer.data))

class Property_Sub_CategoryAdminAPI(APIView):
    def get(self, request, format=None):
        search = request.GET.get('search')
        if search:
            multiple_q = Q(property_sub_category_Name__icontains = search)
            listingobj = Property_Sub_Category.objects.filter(multiple_q)
        else:
            listingobj = Property_Sub_Category.objects.all()
        serializer = PropertySubCategoryAdminSerializer(listingobj, many=True)
        return Response(util.success(self, serializer.data))