from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import json
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.core import serializers as core_serializers
from django.views.decorators.csrf import csrf_exempt

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework.parsers import MultiPartParser, FormParser

from accounts.paginatorviews import MyPagination
from .models import *
from accounts.views import get_user_usertype_userprofile
from .serializer import *

from master import util
from datetime import datetime,timedelta
from master.serializer import CitySerializer
from django.db.models import Count

# ===============Residentila=====================
class Residential_property_Pet_Friendly(APIView):
    def get(self,request, format=None):
        try:
            petfriendlyobj=Property_Detail.objects.filter(property_listing_type=1,property_pet_friendly=True).count()
            if petfriendlyobj != 0:
                return Response(util.success(self,petfriendlyobj))
            else:
                return Response(util.error(self,'No data Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class Residential_property_No_Fee(APIView):
    def get(self,request, format=None):
        try:
            nofeeobj=Property_Detail.objects.filter(property_listing_type=1,is_property_fee=False).count()
            # print(nofeeobj)
            if nofeeobj != 0:
                return Response(util.success(self,nofeeobj))
            else:
                return Response(util.error(self,'No data Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class Residential_property_just_listed(APIView):
    def post(self, request, format=None):
        try:
            data=request.data
            if 'current_date' in data:
                date_from = datetime.strptime(data['current_date'], '%Y-%m-%d') - timedelta(hours=24)
                justlisted=Property_Detail.objects.filter(property_listing_type=1,created_date__gte=date_from).count()
                if justlisted != 0:
                    return Response(util.success(self,justlisted))
                else:
                    return Response(util.error(self,'No data Found'))
            else:
                return Response(util.error(self,'current_date is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class luxary_sales_amount(APIView):
    def get(self, request, format=None):
        try:
            salesobj=LuxarySalesAmt.objects.last()
            if salesobj != None:
                listingtypeobj=Propertylisting_type.objects.filter(property_listing_name="Residential")
                proertyobj=Property_Detail.objects.filter(property_listing_type__in=listingtypeobj,property_listing_amount__gte=salesobj.Amt).count()
                if proertyobj!= 0:
                    return Response(util.success(self,proertyobj))
                else:
                    return Response(util.error(self,'No data Found'))
            else:
                return Response(util.error(self,'No data Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class luxary_rent_amount(APIView):
    def get(self, request, format=None):
        try:
            rentobj=LuxaryRentAmt.objects.last()
            if rentobj != None:
                listingtypeobj=Propertylisting_type.objects.filter(property_listing_name="Residential")
                proertyobj=Property_Detail.objects.filter(property_listing_type__in=listingtypeobj,property_listing_amount__gte=rentobj.Amt).count()
                if proertyobj!= 0:
                    return Response(util.success(self,proertyobj))
                else:
                    return Response(util.error(self,'No data Found'))
            else:
                return Response(util.error(self,'No data Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class Vacation_Property(APIView):
    def get(self, request, format=None):
        try:
            if Property_Main_Category.objects.filter(Main_category="Vacation"):
                maincategoryobj=Property_Main_Category.objects.filter(Main_category="Vacation")
                proertyobj=Property_Detail.objects.filter(property_main_category__in=maincategoryobj,property_listing_type=1).count()
                if proertyobj!= 0:
                    return Response(util.success(self,proertyobj))
                else:
                    return Response(util.error(self,'No data Found'))
            else:
                return Response(util.error(self,'No data Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class Foreclouser_Property(APIView):
    def get(self, request, format=None):
        try:
            if Property_Main_Category.objects.filter(Main_category="Foreclosure"):
                maincategoryobj=Property_Main_Category.objects.get(Main_category="Foreclosure")
                proertyobj=Property_Detail.objects.filter(property_main_category=maincategoryobj).count()
                if proertyobj!= 0:
                    return Response(util.success(self,proertyobj))
                else:
                    return Response(util.error(self,'No data Found'))
            else:
                return Response(util.error(self,'No data Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class Ofiice_Property(APIView):
    def get(self, request, format=None):
        try:
            if Property_Main_Category.objects.filter(Main_category="Office"):
                maincategoryobj=Property_Main_Category.objects.filter(Main_category="Office")
                proertyobj=Property_Detail.objects.filter(property_main_category__in=maincategoryobj,property_listing_type=2).count()
                if proertyobj!= 0:
                    return Response(util.success(self,proertyobj))
                else:
                    return Response(util.error(self,'No data Found'))
            else:
                return Response(util.error(self,'No data Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class Retail_Property(APIView):
    def get(self, request, format=None):
        try:
            if Property_Main_Category.objects.filter(Main_category="Retail"):
                maincategoryobj=Property_Main_Category.objects.filter(Main_category="Retail")
                proertyobj=Property_Detail.objects.filter(property_main_category__in=maincategoryobj,property_listing_type=2).count()
                if proertyobj!= 0:
                    return Response(util.success(self,proertyobj))
                else:
                    return Response(util.error(self,'No data Found'))
            else:
                return Response(util.error(self,'No data Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class Mixedused_Propety(APIView):
    def get(self, request, format=None):
        try:
            if Property_Main_Category.objects.filter(Main_category="Mixed Use"):
                maincategoryobj=Property_Main_Category.objects.filter(Main_category="Mixed Use")
                proertyobj=Property_Detail.objects.filter(property_main_category__in=maincategoryobj,property_listing_type=2).count()
                if proertyobj!= 0:
                    return Response(util.success(self,proertyobj))
                else:
                    return Response(util.error(self,'No data Found'))
            else:
                return Response(util.error(self,'No data Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class Industrial_property(APIView):
    def get(self, request, format=None):
        try:
            if Property_Main_Category.objects.filter(Main_category="Industrial"):
                maincategoryobj=Property_Main_Category.objects.filter(Main_category="Industrial")
                proertyobj=Property_Detail.objects.filter(property_main_category__in=maincategoryobj,property_listing_type=2).count()
                if proertyobj!= 0:
                    return Response(util.success(self,proertyobj))
                else:
                    return Response(util.error(self,'No data Found'))
            else:
                return Response(util.error(self,'No data Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class Land_property(APIView):
    def get(self, request, format=None):
        try:
            if Property_Main_Category.objects.filter(Main_category="Land"):
                maincategoryobj=Property_Main_Category.objects.filter(Main_category="Land")
                proertyobj=Property_Detail.objects.filter(property_main_category__in=maincategoryobj,property_listing_type=2).count()
                if proertyobj!= 0:
                    return Response(util.success(self,proertyobj))
                else:
                    return Response(util.error(self,'No data Found'))
            else:
                return Response(util.error(self,'No data Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class Commercial_property_just_listed(APIView):
    def post(self, request, format=None):
        try:
            data=request.data
            if 'current_date' in data:
                date_from = datetime.strptime(data['current_date'], '%Y-%m-%d') - timedelta(hours=24)
                justlisted=Property_Detail.objects.filter(property_listing_type=2,created_date__gte=date_from).count()
                if justlisted != 0:
                    return Response(util.success(self,justlisted))
                else:
                    return Response(util.error(self,'No data Found'))
            else:
                return Response(util.error(self,'current_date is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

from geopy.geocoders import Nominatim

def get_city_name(latitude, longitude):
    geolocator = Nominatim(user_agent="myapp")
    location = geolocator.reverse(str(latitude) + ", " + str(longitude))
    # return location.raw
    return location.raw['address']['suburb']

class Residential_Nearest_property(APIView):
    def post(self, request, fromat=None):
        listingtypeobj=Propertylisting_type.objects.filter(property_listing_name="Residential")
        data = request.data
        if 'latitude' in data and 'longitude' in data:
            city = get_city_name(data['latitude'], data['longitude'])
            if CityMaster.objects.filter(city_name = city):
                cityobj1=CityMaster.objects.get(city_name = city)
                stateobj=StateMaster.objects.get(id=cityobj1.state_master.id)
                statewisecity=CityMaster.objects.filter(state_master=stateobj)
                propertyobj=Property_Detail.objects.filter(property_city__in=statewisecity, property_listing_type__in=listingtypeobj)
                cityproperty={}
                for i in propertyobj:
                    if i.property_city.city_name in cityproperty:
                        cityproperty[i.property_city.city_name] += 1
                    else:
                        cityproperty[i.property_city.city_name] = 1
                citydetail= CityMaster.objects.filter(city_name__in=cityproperty.keys())
                serializers=CitySerializer(citydetail, many=True)
                if serializers.data:
                    return Response(util.success(self,serializers.data))
                else:
                    propertyobj=Property_Detail.objects.filter(property_listing_type__in=listingtypeobj)[:8]
                    city_obj=[]
                    for i in propertyobj:
                        city_obj.append(i.property_city.id)
                    cityid=CityMaster.objects.filter(id__in=city_obj)
                    serializers=CitySerializer(cityid, many=True)
                    return Response(util.success(self,serializers.data))
            else:
                propertyobj=Property_Detail.objects.filter(property_listing_type__in=listingtypeobj)[:8]
                city_obj=[]
                for i in propertyobj:
                    # print(i.property_city.id)
                    city_obj.append(i.property_city.id)
                # print(city_obj)
                cityid=CityMaster.objects.filter(id__in=city_obj)
                serializers=CitySerializer(cityid, many=True)
                return Response(util.success(self,serializers.data))
        else:
            propertyobj=Property_Detail.objects.filter(property_listing_type__in=listingtypeobj)[:8]
            city_obj=[]
            for i in propertyobj:
                city_obj.append(i.property_city.id)
            cityid=CityMaster.objects.filter(id__in=city_obj)
            serializers=CitySerializer(cityid, many=True)
            return Response(util.success(self,serializers.data))

class Commercial_Nearest_property(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        try:
            data=request.data
            listingtypeobj=Propertylisting_type.objects.filter(property_listing_name="Commercial")
            if 'latitude' in data and 'longitude' in data:
                city = get_city_name(data['latitude'], data['longitude'])
                if CityMaster.objects.filter(city_name = city):
                    cityobj1=CityMaster.objects.get(city_name=city)
                    stateobj=StateMaster.objects.get(id=cityobj1.state_master.id)
                    statewisecity=CityMaster.objects.filter(state_master=stateobj)
                    propertyobj=Property_Detail.objects.filter(property_city__in=statewisecity, property_listing_type__in=listingtypeobj)

                    cityproperty={}
                    for i in propertyobj:
                        if i.property_city.city_name in cityproperty:
                            cityproperty[i.property_city.city_name] += 1
                        else:
                            cityproperty[i.property_city.city_name] = 1
                    citydetail= CityMaster.objects.filter(city_name__in=cityproperty.keys())
                    serializers=CitySerializer(citydetail, many=True)
                    if serializers.data:
                        return Response(util.success(self,serializers.data))
                    else:
                        propertyobj=Property_Detail.objects.filter(property_listing_type__in=listingtypeobj)[:8]
                        city_obj=[]
                        for i in propertyobj:
                            city_obj.append(i.property_city.id)
                        cityid=CityMaster.objects.filter(id__in=city_obj)
                        serializers=CitySerializer(cityid, many=True)
                        return Response(util.success(self,serializers.data))
                else:
                    propertyobj=Property_Detail.objects.filter(property_listing_type__in=listingtypeobj)[:8]
                    city_obj=[]
                    for i in propertyobj:
                        city_obj.append(i.property_city.id)
                    cityid=CityMaster.objects.filter(id__in=city_obj)
                    serializers=CitySerializer(cityid, many=True)
                    return Response(util.success(self,serializers.data))
            else:
                propertyobj=Property_Detail.objects.filter(property_listing_type__in=listingtypeobj)[:8]
                # print(propertyobj)
                city_obj=[]
                for i in propertyobj:
                    city_obj.append(i.property_city.id)
                cityid=CityMaster.objects.filter(id__in=city_obj)
                serializers=CitySerializer(cityid, many=True)
                return Response(util.success(self,serializers.data))
        except Exception as e:
            return Response(util.error(self,str(e)))
# ======================check nearest property=======================
class Recidential_check_property(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            user_id=request.GET.get('user_id',None)
            data=request.data
            if 'city_id' in data:
                if CityMaster.objects.filter(id=data['city_id']):
                    cityobj1=CityMaster.objects.get(id=data['city_id'])
                    propertylistingobj=Propertylisting_type.objects.filter(property_listing_name="Residential")
                    propertydetailobj=Property_Detail.objects.filter(property_city=cityobj1,property_listing_type__in=propertylistingobj)
                    
                    paginator = MyPagination()
                    paginated_queryset = paginator.paginate_queryset(propertydetailobj, request)
                    serializers=PropertySerializer(paginated_queryset, context={'user_id': user_id}, many=True)
                    if serializers.data:
                        return Response(util.success(self,serializers.data))
                    else:
                        return Response(util.error(self,"No Data Found"))
                return Response(util.error(self,"No Data Found"))
            return Response(util.error(self, 'city_id is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class Commercial_check_property(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            user_id=request.GET.get('user_id',None)
            data=request.data
            if 'city_id' in data:
                if CityMaster.objects.filter(id=data['city_id']):
                    cityobj1=CityMaster.objects.get(id=data['city_id'])
                    propertylistingobj=Propertylisting_type.objects.filter(property_listing_name="Commercial")
                    propertydetailobj=Property_Detail.objects.filter(property_city=cityobj1,property_listing_type__in=propertylistingobj)
                    paginator = MyPagination()
                    paginated_queryset = paginator.paginate_queryset(propertydetailobj, request)
                    serializers=PropertySerializer(paginated_queryset, context={'user_id': user_id}, many=True)
                    if serializers.data:
                        return Response(util.success(self,serializers.data))
                    else:
                        return Response(util.error(self,"No Data Found"))
                return Response(util.error(self,"No Data Found"))
            return Response(util.error(self, 'city_id is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

# ======================Property Filter========================================
class PropertyRescidentialFilter(APIView):
    def post(self,request,format=None):
        try:
            user_id=request.GET.get('user_id',None)
            data=request.data
            if 'property_main_category' in data:
                if Property_Main_Category.objects.filter(id=data['property_main_category']):
                    propertymaincategoryobj=Property_Main_Category.objects.get(id=data['property_main_category']) # get Property_Main_Category objects
                    propertylistingtype=Property_Listing_Type.objects.get(id=propertymaincategoryobj.listing_type.id) # get Property_Listing_Type objects
                    propertytypeobj=Propertylisting_type.objects.get(id=propertylistingtype.type_of_listing.id) # get Propertylisting_Type objects
                    propertydetailobj=Property_Detail.objects.filter(property_listing_type=propertytypeobj)
                    if data['bedrooms'] != None:
                        propertydetailobj=propertydetailobj.filter(Bedrooms=data['bedrooms'])
                    if data['bathrooms'] != None:
                        propertydetailobj=propertydetailobj.filter(Bathrooms=data['bathrooms'])
                    if data['squft_min'] != None or data['squft_max'] != None:
                        propertydetailobj=propertydetailobj.filter(Square_sqft__lte=data['squft_max'])
                        propertydetailobj=propertydetailobj.filter(Square_sqft__gte=data['squft_min'])
                    if data['price_min'] != None or data['price_max'] != None:
                        propertydetailobj=propertydetailobj.filter(property_listing_amount__lte=data['price_max'])
                        propertydetailobj=propertydetailobj.filter(property_listing_amount__gte=data['price_min'])
                    if data['amenities_filter'] != None:
                        property_detail_obj_id=propertydetailobj.values_list('id',flat=True)
                        propertyobj=Property_Amenities.objects.filter(property_details__in=property_detail_obj_id)
                        propertyobj=propertyobj.filter(amenites_master__in=data['amenities_filter'])
                        serializer1=PropertyAmenitiesSerializer(propertyobj, many=True)
                        if serializer1.data:
                            return Response(util.success(self,serializer1.data))
                    else:
                        paginator = MyPagination()
                        paginated_queryset = paginator.paginate_queryset(propertydetailobj, request)
                        # serializer = PropertySerializer(paginated_queryset, context={'request': request}, many=True)
                        serializer2=PropertySerializer(paginated_queryset, context={'user_id': user_id}, many=True)
                        # serializer2=PropertyDetailSerializer(propertydetailobj, many=True)
                        return Response(util.success(self,serializer2.data))
                else:
                    return Response(util.error(self, 'no data found'))
            else:
                return Response(util.error(self,'property_main_category is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class PropertyCommercialFilter(APIView):
    def post(self, request, format=None):
        try:
            user_id=request.GET.get('user_id',None)
            data=request.data
            if 'property_main_category' in data:
                if Property_Main_Category.objects.filter(id=data['property_main_category']):
                    propertymaincategoryobj=Property_Main_Category.objects.get(id=data['property_main_category']) # get Property_Main_Category objects
                    if propertymaincategoryobj.Main_category == "Leisure":
                        if 'Sub_category' in data:
                            propertysubcategoryobj=Property_Sub_Category.objects.get(id=data['Sub_category'])
                            propertydetailobj=Property_Detail.objects.filter(property_sub_category=propertysubcategoryobj.id)
                        else:
                            return Response(util.error(self,'Sub_category is needed'))
                    else:
                        propertylistingtype=Property_Listing_Type.objects.get(id=propertymaincategoryobj.listing_type.id) # get Property_Listing_Type objects
                        propertytypeobj=Propertylisting_type.objects.get(id=propertylistingtype.type_of_listing.id) # get Propertylisting_Type objects
                        propertydetailobj=Property_Detail.objects.filter(property_listing_type=propertytypeobj.id)

                    if data['Units']!=None:
                        propertydetailobj=propertydetailobj.filter(Units=data['Units'])
                    if data['Room']!=None:
                        propertydetailobj=propertydetailobj.filter(Rooms=data['Room'])
                    if data['Sqft_Min'] != None or data['Sqft_Max'] != None:
                        propertydetailobj=propertydetailobj.filter(Square_sqft__gte=data['Sqft_Max'])
                        propertydetailobj=propertydetailobj.filter(Square_sqft__gte=data['Sqft_Min'])
                    if data['Block']:
                        propertydetailobj=propertydetailobj.filter(Block=data['Block'])
                    if data['Lot']:
                        propertydetailobj=propertydetailobj.filter(Lot=data['Lot'])
                    if data['Zone']:
                        propertydetailobj=propertydetailobj.filter(Zone=data['Zone'])
                    if data['Lot_Dimensions']:
                        propertydetailobj=propertydetailobj.filter(Lot_Dimensions=data['Lot_Dimensions'])
                    if data['Building_Dimensions']:
                        propertydetailobj=propertydetailobj.filter(Building_Dimension=data['Building_Dimensions'])
                    if data['Stories']:
                        propertydetailobj=propertydetailobj.filter(Stories=data['Stories'])
                    if data['FAR']:
                        propertydetailobj=propertydetailobj.filter(FAR=data['FAR'])
                    if data['Assessment']:
                        propertydetailobj=propertydetailobj.filter(Assessment=data['Assessment'])
                    if data['Annual_Taxes']:
                        propertydetailobj=propertydetailobj.filter(Annual_Taxes=data['Annual_Taxes'])
                    if data['Available_Air_Rights']:
                        propertydetailobj=propertydetailobj.filter(Available_Air_Rights=data['Available_Air_Rights'])
                    if data['Cost_type']==1: # Total Monthly cost
                        if data['Price_Min']!=None or data['Price_Max'] != None:
                            propertydetailobj=propertydetailobj.filter(property_listing_amount__lte=data['Price_Max'])
                            propertydetailobj=propertydetailobj.filter(property_listing_amount__gte=data['Price_Min'])
                    elif data['Cost_type']==2:
                        if data['Price_Min']!=None or data['Price_Max'] != None:
                            propertydetailobj=propertydetailobj.filter(property_cost_per_sq__lte=data['Price_Max'])
                            propertydetailobj=propertydetailobj.filter(property_cost_per_sq__gte=data['Price_Min'])
                    
                    paginator = MyPagination()
                    paginated_queryset = paginator.paginate_queryset(propertydetailobj, request)
                    serializer = PropertySerializer(paginated_queryset, context={'user_id': user_id}, many=True)
                    if serializer.data:
                        return Response(util.success(self, serializer.data))
                    else:
                        return Response(util.error(self,'no data found'))
                else:
                    return Response(util.error(self, 'no data found'))
            else:
                return Response(util.error(self, 'property_main_category is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

# ABCDFSH

class search_filter(APIView):
    def post(self, request, format = None):
        try:
            # user_id = request.GET.get("user_id",None)
            user_id = request.data.get("user_id")
            # Residential and Commercial======(id)
            propertylistingtypeobj = request.data.get('property_listing')
            if Propertylisting_type.objects.filter(id=propertylistingtypeobj):
                listingtypeob = Propertylisting_type.objects.get(id=propertylistingtypeobj)
            else:
                listingtypeob = None
            
            # rent , buy , sales, leasing, etc.========(id)
            categoryid = request.data.get('category')
            if Property_Listing_Type.objects.filter(id=categoryid):
                categoryobj = Property_Listing_Type.objects.get(id=categoryid)
            else:
                categoryobj = None
            
            # Main Category (id)
            typeid = request.data.get('type')
            if Property_Main_Category.objects.filter(id=typeid):
                tyepobj = Property_Main_Category.objects.get(id=typeid)
            else:
                tyepobj = None
            
            # Area Master
            areaid = request.data.get('area')
            if AreaMaster.objects.filter(id=areaid):
                areaobj = AreaMaster.objects.get(id=areaid)
            else:
                areaobj = None
            
            # City Master
            cityid = request.data.get('city')
            if CityMaster.objects.filter(id=cityid):
                cityobj = CityMaster.objects.get(id=cityid)
            else:
                cityobj = None

            # State Master
            stateid = request.data.get('state')
            if StateMaster.objects.filter(id=stateid):
                stateobj = StateMaster.objects.get(id=stateid)
            else:
                stateobj = None
            
            # Country Master
            countryid = request.data.get('country')
            if CountryMaster.objects.filter(id=countryid):
                countryobj = CountryMaster.objects.get(id=countryid)
            else:
                countryobj = None
            
            pricemin = request.data.get('pricemin')
            pricemax = request.data.get('pricemax')
            squftmin = request.data.get('Squft_min')
            squftmax = request.data.get('Squft_max')
            filterobj = request.data['filter_obj']
            if listingtypeob is not None and categoryobj is not None:
                if tyepobj != None:
                    if tyepobj.Main_category == "Leisure":
                        Sub_category = request.data.get('Sub_category')
                        propertysubcategoryobj=Property_Sub_Category.objects.get(id=Sub_category)
                        propertyobj = Property_Detail.objects.filter(property_listing_type = listingtypeob.id).filter(propertylisting_type = categoryobj.id).filter(property_main_category = tyepobj).filter(property_sub_category=propertysubcategoryobj).filter(is_property_open = True)
                    else:
                        propertyobj = Property_Detail.objects.filter(property_listing_type = listingtypeob.id).filter(propertylisting_type = categoryobj.id).filter(property_main_category = tyepobj).filter(is_property_open = True)
                else:
                    propertyobj = Property_Detail.objects.filter(property_listing_type = listingtypeob.id).filter(propertylisting_type = categoryobj.id).filter(is_property_open = True)
                if filterobj == False:
                    # Area
                    if areaobj != None and cityobj != None and stateobj != None and countryobj != None:
                        propertyobj=propertyobj.filter(property_area = areaobj.id)
                        if pricemin != None or pricemax != None:
                            propertyobj=propertyobj.filter(property_listing_amount__gte=pricemin).filter(property_listing_amount__lte=pricemax)
                    # City
                    elif areaobj == None and cityobj != None and stateobj != None and countryobj != None:
                        propertyobj=propertyobj.filter(property_city = cityobj.id)
                        if pricemin != None or pricemax != None:
                            propertyobj=propertyobj.filter(property_listing_amount__gte=pricemin).filter(property_listing_amount__lte=pricemax)
                    # State
                    elif areaobj == None and cityobj == None and stateobj != None and countryobj != None:
                        propertyobj=propertyobj.filter(property_state = stateobj.id)
                        if pricemin != None or pricemax != None:
                            propertyobj=propertyobj.filter(property_listing_amount__gte=pricemin).filter(property_listing_amount__lte=pricemax)
                    # Country
                    elif areaobj == None and cityobj == None and stateobj == None and countryobj != None:
                        state_obj = StateMaster.objects.filter(country_master = countryobj.id).values_list('id', flat=True)
                        propertyobj = propertyobj.filter(property_state__in = state_obj)
                        if pricemin != None or pricemax != None:
                            propertyobj=propertyobj.filter(property_listing_amount__gte=pricemin).filter(property_listing_amount__lte=pricemax)
                    # # Else
                    else:
                        if pricemin != None or pricemax != None:
                            propertyobj=propertyobj.filter(property_listing_amount__gte=pricemin).filter(property_listing_amount__lte=pricemax)
                else:
                    if listingtypeob.property_listing_name == 'Residential':
                        bedrooms = request.data.get('Bedrooms')
                        bathrooms = request.data.get('Bathrooms')
                        amenities = request.data.get('Amenities_filter')
                        # Area
                        if areaobj != None and cityobj != None and stateobj != None and countryobj != None:
                            propertyobj=propertyobj.filter(property_area = areaobj.id)
                            if pricemin != None or pricemax != None:
                                propertyobj=propertyobj.filter(property_listing_amount__gte=pricemin).filter(property_listing_amount__lte=pricemax)
                            if squftmin != None or squftmax != None:
                                propertyobj=propertyobj.filter(Square_sqft__gte=squftmin).filter(Square_sqft__lte=squftmax)
                        # City
                        elif areaobj == None and cityobj != None and stateobj != None and countryobj != None:
                            propertyobj=propertyobj.filter(property_city = cityobj.id)
                            if pricemin != None or pricemax != None:
                                propertyobj=propertyobj.filter(property_listing_amount__gte=pricemin).filter(property_listing_amount__lte=pricemax)
                            if squftmin != None or squftmax != None:
                                propertyobj=propertyobj.filter(Square_sqft__gte=squftmin).filter(Square_sqft__lte=squftmax)
                        # State
                        elif areaobj == None and cityobj == None and stateobj != None and countryobj != None:
                            propertyobj=propertyobj.filter(property_state__in = stateobj.id)
                            if pricemin != None or pricemax != None:
                                propertyobj=propertyobj.filter(property_listing_amount__gte=pricemin).filter(property_listing_amount__lte=pricemax)
                            if squftmin != None or squftmax != None:
                                propertyobj=propertyobj.filter(Square_sqft__gte=squftmin).filter(Square_sqft__lte=squftmax)
                        # Country
                        elif areaobj == None and cityobj == None and stateobj == None and countryobj != None:
                            state_obj = StateMaster.objects.filter(country_master = countryobj.id)
                            propertyobj = propertyobj.filter(property_state__in = state_obj)
                            if pricemin != None or pricemax != None:
                                propertyobj=propertyobj.filter(property_listing_amount__gte=pricemin).filter(property_listing_amount__lte=pricemax)
                            if squftmin != None or squftmax != None:
                                propertyobj=propertyobj.filter(Square_sqft__gte=squftmin).filter(Square_sqft__lte=squftmax)
                        # Else
                        else:
                            if pricemin != None or pricemax != None:
                                propertyobj=propertyobj.filter(property_listing_amount__gte=pricemin).filter(property_listing_amount__lte=pricemax)
                            if squftmin != None or squftmax != None:
                                propertyobj=propertyobj.filter(Square_sqft__gte=squftmin).filter(Square_sqft__lte=squftmax)
                        
                        if bedrooms != None:
                           propertyobj = propertyobj.filter(Bedrooms__gte = bedrooms)
                           # print(propertyobj)
                        if bathrooms != None:
                           propertyobj = propertyobj.filter(Bathrooms__gte = bathrooms)
                        if amenities != None:
                            property_detail_obj_id=propertyobj.values_list('id',flat=True)
                            property_obj=Property_Amenities.objects.filter(property_details__in=property_detail_obj_id).filter(amenites_master__in=amenities)
                        else:
                            property_obj=None
                    elif listingtypeob.property_listing_name == 'Commercial':
                        unit = request.POST.get('units')
                        room = request.POST.get('room')
                        block = request.POST.get('block')
                        lot = request.POST.get('lot')
                        zone = request.POST.get('Zone')
                        lot_dimension = request.POST.get('lot_diamensions')
                        building_dimension = request.POST.get('building_diamensions')
                        stories = request.POST.get('stories')
                        far = request.POST.get('far')
                        assessment = request.POST.get('Assessment')
                        annual_taxes = request.POST.get('Annual_Taxes')
                        available_air_rights = request.POST.get('Available_Air_Rights')
                        # Area
                        if areaobj != None and cityobj != None and stateobj != None and countryobj != None:
                            propertyobj=propertyobj.filter(property_area = areaobj.id)
                            if pricemin != None or pricemax != None:
                                propertyobj=propertyobj.filter(property_listing_amount__gte=pricemin).filter(property_listing_amount__lte=pricemax)
                            if squftmin != None or squftmax != None:
                                propertyobj=propertyobj.filter(Square_sqft__gte=squftmin).filter(Square_sqft__lte=squftmax)
                        # City
                        elif areaobj == None and cityobj != None and stateobj != None and countryobj != None:
                            propertyobj=propertyobj.filter(property_city = cityobj.id)
                            if pricemin != None or pricemax != None:
                                propertyobj=propertyobj.filter(property_listing_amount__gte=pricemin).filter(property_listing_amount__lte=pricemax)
                            if squftmin != None or squftmax != None:
                                propertyobj=propertyobj.filter(Square_sqft__gte=squftmin).filter(Square_sqft__lte=squftmax)
                        # State
                        elif areaobj == None and cityobj == None and stateobj != None and countryobj != None:
                            propertyobj=propertyobj.filter(property_state__in = stateobj.id)
                            if pricemin != None or pricemax != None:
                                propertyobj=propertyobj.filter(property_listing_amount__gte=pricemin).filter(property_listing_amount__lte=pricemax)
                            if squftmin != None or squftmax != None:
                                propertyobj=propertyobj.filter(Square_sqft__gte=squftmin).filter(Square_sqft__lte=squftmax)
                        # Country
                        elif areaobj == None and cityobj == None and stateobj == None and countryobj != None:
                            state_obj = StateMaster.objects.filter(country_master = countryobj.id)
                            propertyobj = propertyobj.filter(property_state__in = state_obj)
                            if pricemin != None or pricemax != None:
                                propertyobj=propertyobj.filter(property_listing_amount__gte=pricemin).filter(property_listing_amount__lte=pricemax)
                            if squftmin != None or squftmax != None:
                                propertyobj=propertyobj.filter(Square_sqft__gte=squftmin).filter(Square_sqft__lte=squftmax)
                        # Else
                        else:
                            if pricemin != None or pricemax != None:
                                propertyobj=propertyobj.filter(property_listing_amount__gte=pricemin).filter(property_listing_amount__lte=pricemax)
                            if squftmin != None or squftmax != None:
                                propertyobj=propertyobj.filter(Square_sqft__gte=squftmin).filter(Square_sqft__lte=squftmax)
                        
                        if unit != None:
                            propertyobj = propertyobj.filter(Units__gte = unit)
                        if room != None:
                            propertyobj = propertyobj.filter(Rooms__gte = room)
                        if block != None:
                            propertyobj = propertyobj.filter(Block__gte = block)
                        if lot != None:
                            propertyobj = propertyobj.filter(Lot__gte = lot)
                        if zone != None:
                            propertyobj = propertyobj.filter(Zone__gte = zone)
                        if lot_dimension != None:
                            propertyobj = propertyobj.filter(Lot_Dimensions__gte = lot_dimension)
                        if building_dimension != None:
                            propertyobj = propertyobj.filter(Building_Dimension__gte = building_dimension)
                        if stories != None:
                            propertyobj = propertyobj.filter(Stories__gte = stories)
                        if far != None:
                            propertyobj = propertyobj.filter(FAR__gte = far)
                        if assessment != None:
                            propertyobj = propertyobj.filter(Assessment__gte = assessment)
                        if annual_taxes != None:
                            propertyobj = propertyobj.filter(Annual_Taxes__gte = annual_taxes)
                        if available_air_rights != None:
                            propertyobj = propertyobj.filter(Available_Air_Rights__gte = available_air_rights)
                
                cityidnb = []
                for i in propertyobj:
                    if i.property_city.id not in cityidnb:
                        cityidnb.append(i.property_city.id)
                    else:
                        pass
                
                areaidnb = AreaMaster.objects.filter(city_master__in = cityidnb)
                nbspuser=[]
                for areaid in areaidnb:
                    neighbourhood_spicialityobj=Nb_specality_area.objects.filter(area_id__icontains = areaid.id,is_verified = "Approve")
                    for j in neighbourhood_spicialityobj:
                        neighbourhood_spicialityid=Nb_specality_area.objects.get(id = j.id)
                        if neighbourhood_spicialityid.user.id not in nbspuser:
                            nbspuser.append(neighbourhood_spicialityid.user.id)
                        else:
                            pass
                
                userobj = User.objects.filter(id__in=nbspuser)
                usertypeobj = UserType.objects.filter(user__in=userobj)
                userprofileobj = UserProfile.objects.filter(user_type__in=usertypeobj)
                nbserializer = NeighborAvaliableProfileSerializer(userprofileobj, many=True)


                propertyobjid = Property_Detail.objects.filter(id__in = propertyobj).values_list('user_profile', flat=True)
                userprofileid = UserProfile.objects.filter(id__in = propertyobjid).values_list('user_type', flat=True)
                usertypeid = UserType.objects.filter(id__in = userprofileid).values_list('user', flat=True)

                lice_user = []
                licobj = AgentLic.objects.filter(user__in = usertypeid)
                for license in licobj:
                    if license.is_validated:
                        lice_user.append(license.user.id)
                    else:
                        pass
                
                user_obj = User.objects.filter(id__in = lice_user)
                usertype_obj = UserType.objects.filter(user__in = user_obj)
                userprofileid_obj = UserProfile.objects.filter(user_type__in = usertype_obj).values_list("id", flat=True)
                
                propertyobj = propertyobj.filter(user_profile__in = userprofileid_obj)
                

                paginator = MyPagination()
                paginated_queryset = paginator.paginate_queryset(propertyobj, request)
                serializer = PropertySerializer(paginated_queryset, context={'user_id': user_id}, many=True)
                # serializer1=PropertyAmenitiesSerializer(property_obj, many=True)
                if serializer.data:
                    # if serializer1.data:
                        # return Response(util.success(self,[serializer.data,serializer1.data]))
                    # print(areaobj)
                    if areaobj:
                        return Response(util.success(self,{"porperty":serializer.data,"page":2,"Neighborhood":nbserializer.data}))
                    else:
                        return Response(util.success(self,{"porperty":serializer.data,"page":1,"Neighborhood":nbserializer.data}))
                else:
                    return Response(util.error(self, 'No Data Found'))
            else:
                return Response(util.error(self, "property_listing, category is required"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class Home_Card_Title(APIView):
    def get(self, request, format=None):
        try:
            homecardtitleobj=HomeCardTitle.objects.last()
            serializer=HomeCardTitleSerializer(homecardtitleobj) 
            if serializer.data:
                return Response(util.success(self, serializer.data))
            else:
                return Response(util.error(self, 'data not found'))
        except Exception as e:
            return Response(util.error(self,str(e)))           

class Home_Card(APIView):
    def get(self, request, format=None):
        try:
            homecardtitleobj=HomeCard.objects.all()
            serializer=HomeCardSerializer(homecardtitleobj, many=True) 
            if serializer.data:
                return Response(util.success(self, serializer.data))
            else:
                return Response(util.error(self, 'data not found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class FindAreaCityState(APIView):
    def post(self, request, format = None):
        try:
            zipcodeobj = request.data.get('zipcode')
            if zipcodeobj:
                zipobj = ZipCodeMaster.objects.filter(Zipcode = zipcodeobj).values_list("area_master", flat=True)
                areaobj = AreaMaster.objects.filter(id__in = zipobj)
                cityobj = []
                stateobj = []
                for i in areaobj:
                    if i.city_master.id not in cityobj:
                        cityobj.append(i.city_master.id)
                    else:
                        pass
                    
                    if i.city_master.state_master.id not in stateobj:
                        stateobj.append(i.city_master.state_master.id)
                    else:
                        pass
                cityid = CityMaster.objects.filter(id__in = cityobj)
                stateid = StateMaster.objects.filter(id__in = stateobj)

                areaserializer = AreaSerializer(areaobj, many=True)
                cityserializer = CitySerializer(cityid, many=True)
                stateserializer = StateSerializer(stateid, many=True)

                return Response(util.success(self, {"town":areaserializer.data, "city":cityserializer.data, "state":stateserializer.data}))
            else:
                return Response(util.error(self, 'zipcode not found'))
        except Exception as e:
            return Response(util.error(self,str(e)))