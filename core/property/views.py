from fileinput import filename
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.core import serializers as core_serializers
from django.views.decorators.csrf import csrf_exempt

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.db.models import Avg
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework.parsers import MultiPartParser, FormParser

from accounts.paginatorviews import MyPagination
from virtual_office.models import customer_info
from virtual_office.models import VirtualOffice, VirtualOfficeTeam,Signed_Documnets_Custom_Info
from .models import *
from accounts.views import get_user_usertype_userprofile
from .serializer import *
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils import timezone
from master import util
from django.conf import settings
from django.shortcuts import render, redirect
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import base64
from django.core.files.base import ContentFile
from accounts.views import get_tokens_for_user
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
from django.db.models import Q
from virtual_office.serializer import DocumentSerializers,ShareDocumentSerializers,CustomerListSerializer
from django.core.mail import send_mail
from django.db.models import Max

class PropertyMainCategory(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            data = json.loads(request.body)
            if 'userid' in data and 'Category_name' in data and 'is_active' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['userid'])
                if usertype.user_type==0:

                    Property_Main_Category.objects.create(
                        Category_name=data['Category_name'],is_active=data['is_active']
                    )
                    # return Response({'msg':'Main Category Created'})
                    return Response(util.success(self,'Main Category Created'))
                else:
                    # return Response({'msg':'Your Not Valid User to Create the Property'})
                    return Response(util.error(self,'Your Not Valid User to Create the Property'))
            else:
                # return Response({'msg':'Category_name and is_active needed'})
                return Response(util.error(self,'Category_name and is_active needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))
    
    def put(self, request, format=None):
        try:
            data =json.loads(request.body)
            if 'userid' in data and 'Category_id' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['userid'])
                if Property_Main_Category.objects.filter(id=data['Category_id']):
                    property_main_obj=Property_Main_Category.objects.get(id=data['Category_id'])
                    if usertype.user_type==0:
                        if 'Category_name' in data:
                            property_main_obj.Category_name=data['Category_name']
                            property_main_obj.save()
                            # return Response({'msg':'Category_name updated successfully'})
                            return Response(util.success(self,'Category_name updated successfully'))

                        elif 'is_active' in data:
                            property_main_obj.is_active=data['is_active']
                            property_main_obj.save()
                            # return Response({'msg':'Property Main Category Active Status updated successfully'})
                            return Response(util.success(self,'Property Main Category Active Status updated successfully'))

                        else:
                            # return Response({'msg':'Category_name and is_active needed'})
                            return Response(util.error(self,'Category_name and is_active needed'))
                    else:
                        # return Response({'msg':'Your Not Valid User to Create the Property'})
                        return Response(util.error(self,'Your Not Valid User to Create the Property'))
                else:
                    # return Response({'msg':'Category id is not valid'})
                    return Response(util.error(self,'Category id is not valid'))

            # return Response({'msg':'userid and Category_id needed'})
            return Response(util.error(self,'userid and Category_id needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

    def delete(self, request, format=None):
        try:
            data =json.loads(request.body)
            user,usertype,userprofile=get_user_usertype_userprofile(request,data['userid'])
            if usertype.user_type==0:
                if Property_Main_Category.objects.filter(id=data['Category_id']):
                    property_main_obj=Property_Main_Category.objects.get(id=data['Category_id'])
                    property_main_obj.delete()
                    # return Response({'msg':'property main Category deleted'})
                    return Response(util.success(self,'property main Category deleted'))
                else:
                    # return Response({'msg':'Property main category id not found'})
                    return Response(util.error(self,'Property main category id not found'))
            else:
                # return Response({'msg':'Not a valid user for deleting the property'})
                return Response(util.error(self,'Not a valid user for deleting the property'))
        except Exception as e:
            return Response(util.error(self,str(e)))
    
    def get(self,request, format=None, id=None):
        try:
            propertymaincategoryobj=Property_Main_Category.objects.all()
            serializer=PropertyMainCategorySerializer(propertymaincategoryobj, many=True)
            # return JsonResponse(serializer.data, safe=False)
            if serializer.data:
                return Response(util.success(self,serializer.data))
            else:
                return Response(util.error(self, "No Data Found"))
        except Exception as e:
            return Response(util.error(self,str(e)))
     
class PropertySubCategory(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            data = json.loads(request.body)
            if 'userid' in data and 'Sub_Category_name' in data and 'Main_Category_id' in data and 'is_active' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['userid'])
                if usertype.user_type==0:
                    if Property_Main_Category.objects.filter(id=data["Main_Category_id"]):
                        propertymaincategoryobj=Property_Main_Category.objects.get(id=data["Main_Category_id"])
                        Property_Sub_Category.objects.create(property_main_category=propertymaincategoryobj,property_sub_category_Name=data["Sub_Category_name"],is_active=data['is_active'])
                        # return Response({'msg':'Sub Category Created'})
                        return Response(util.success(self,'Sub Category Created'))
                    else:
                        # return Response({'msg':'Not A Valid Property Main Category Id'})
                        return Response(util.error(self,'Not A Valid Property Main Category Id'))
                else:
                    # return Response({'msg':'Your Not Valid User to Create the Property'})
                    return Response(util.error(self,'Your Not Valid User to Create the Property'))
            else:
                # return Response({'msg':'Category_name and is_active needed'})
                return Response(util.error(self,'Category_name and is_active needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))
    
    def put(self, request, format=None):
        try:
            data =json.loads(request.body)
            if 'userid' in data and 'Sub_Category_id' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['userid'])
                if Property_Sub_Category.objects.filter(id=data['Sub_Category_id']):
                    Property_Sub_Category_Obj=Property_Sub_Category.objects.get(id=data['Sub_Category_id'])
                    if usertype.user_type==0:
                        if 'Sub_Category_name' in data:
                            Property_Sub_Category_Obj.property_sub_category_Name=data['Sub_Category_name']
                            Property_Sub_Category_Obj.save()
                            # Response({'msg':'Sub Category name updated successfully'})
                            Response(util.success(self,'Sub Category name updated successfully'))
                        elif 'is_active' in data:
                            Property_Sub_Category_Obj.is_active=data['is_active']
                            Property_Sub_Category_Obj.save()
                            # return Response({'msg':'Property Sub Category Active Status updated successfully'})
                            return Response(util.success(self,'Property Sub Category Active Status updated successfully'))
                        else:
                            # return Response({'msg':'Sub_Category_name Or is_active needed'})
                            return Response(util.error(self,'Sub_Category_name Or is_active needed'))
                    else:
                        # return Response({'msg':'Your Not Valid User to Create the Property'})
                        return Response(util.error(self,'Your Not Valid User to Create the Property'))
                else:
                    # return Response({'msg':'Sub Category id is not valid'})
                    return Response(util.error(self,'Sub Category id is not valid'))
            # return Response({'msg':'userid and Sub_Category_id needed'})
            return Response(util.error(self,'userid and Sub_Category_id needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

    def delete(self, request, format=None):
        try:
            data =json.loads(request.body)
            if 'userid' in data and 'Sub_Category_id' in data:  
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['userid'])
                if usertype.user_type==0:
                    if Property_Sub_Category.objects.filter(id=data['Sub_Category_id']):
                        property_main_obj=Property_Sub_Category.objects.get(id=data['Sub_Category_id'])
                        property_main_obj.delete()
                        # return Response({'msg':'property sub category deleted'})
                        return Response(util.success(self,'property sub category deleted'))
                    else:
                        # return Response({'msg':'Property sub category id not found'})
                        return Response(util.error(self,'Property sub category id not found'))
                else:
                    # return Response({'msg':'Not a valid user for deleting the property'})
                    return Response(util.error(self,'Not a valid user for deleting the property'))
            else:
                # return Response({'msg':'userid and Sub_Category_id is needed'})
                return Response(util.error(self,'userid and Sub_Category_id is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

    def get(self,request, format=None, id=None):
        try:
            propertysubcategoryobj=Property_Sub_Category.objects.all()
            serializer=PropertySubCategorySerializer(propertysubcategoryobj, many=True)
            # return JsonResponse(serializer.data, safe=False)
            if serializer.data:
                return Response(util.success(self,serializer.data))
            else:
                return Response(util.error(self,'No Data Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class AmenitiesMaster(APIView):
    def post(self, request, format=None):
        try:
            user_id=request.POST.get('amenities_name')
            amenities_icon=request.FILES.get('amenities_icon')
            amenities_name=request.POST.get('amenities_name')
            amenities_type=request.POST.get('amenities_type')
            is_active = request.POST.get('is_active')

            user,usertype,userprofile=get_user_usertype_userprofile(request,user_id)
            if usertype.user_type==0:
                if amenities_icon!=None and amenities_name!=None and amenities_type!=None and is_active!=None:
                    Amenities_Master.objects.create(amenities_icon=amenities_icon,amenities_name=amenities_name,amenities_type=amenities_type,is_active=is_active)
                    # return Response({'msg':'Aminities Created Successfully'})
                    return Response(util.success(self,'Aminities Created Successfully'))
                else:
                    # return Response({'msg':'amenities_icon, amenities_name,amenities_type and is_active is needed'})
                    return Response(util.error(self,'amenities_icon, amenities_name,amenities_type and is_active is needed'))
            else:
                # return Response({'msg':'Not a Valid user To create Aminities'})
                return Response(util.error(self,'Not a Valid user To create Aminities'))
        except Exception as e:
            return Response(util.error(self,str(e)))

    def put(self, request, format=None):
        try:
            user_id=request.POST.get('amenities_name')
            amenities_master_id=request.POST.get("amenities_master_id")
            amenities_icon=request.FILES.get('amenities_icon')
            amenities_name=request.POST.get('amenities_name')
            amenities_type=request.POST.get('amenities_type')
            is_active = request.POST.get('is_active')

            user,usertype,userprofile=get_user_usertype_userprofile(request,user_id)
            if usertype.user_type==0:
                if Amenities_Master.objects.filter(id=amenities_master_id):
                    Amenities_Master_obj=Amenities_Master.objects.get(id=amenities_master_id)
                    if amenities_icon:
                        Amenities_Master_obj.amenities_icon=amenities_icon
                    elif amenities_name:
                        Amenities_Master_obj.amenities_name=amenities_name
                    elif amenities_type:
                        Amenities_Master_obj.amenities_type=amenities_type
                    elif is_active:
                        Amenities_Master_obj.is_active=is_active
                    Amenities_Master_obj.save()
                    # return Response({'msg':'Amenities Master updated successfully'})
                    return Response(util.success(self,'Amenities Master updated successfully'))
                else:
                    # return Response({'msg':'Aminity Master Id is not valid'})
                    return Response(util.error(self,'Aminity Master Id is not valid'))
            else:
                # return Response({'msg':'Not a Valid user To update Aminities'})
                return Response(util.error(self,'Not a Valid user To update Aminities'))
        except Exception as e:
            return Response(util.error(self,str(e)))

    def delete(self,request, format=None, id=None):
        try:
            data =json.loads(request.body)
            if 'userid' in data and 'Amenities_Master_id' in data:  
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['userid'])
                if usertype.user_type==0:
                    if Amenities_Master.objects.filter(id=data['Amenities_Master_id']):
                        amenities_master_obj=Amenities_Master.objects.get(id=data['Amenities_Master_id'])
                        amenities_master_obj.delete()
                        # return Response({'msg':' Amenity Master deleted'})
                        return Response(util.success(self,'Amenity Master deleted'))
                    else:
                        # return Response({'msg':'Amenity Maste id not found'})
                        return Response(util.error(self,'Amenity Maste id not found'))
                else:
                    # return Response({'msg':'Not a valid user for deleting the Amenity Master'})
                    return Response(util.error(self,'Not a valid user for deleting the Amenity Master'))
            else:
                # return Response({'msg':'userid and Amenities_Master_id is needed'})
                return Response(util.error(self,'userid and Amenities_Master_id is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

    def get(self,request, format=None):
        try:
            amenitiesmasterobj=Amenities_Master.objects.all()
            serializer=AmenitiesNasterSerializer(amenitiesmasterobj, many=True)
            # return JsonResponse(serializer.data, safe=False)
            if serializer.data:
                return Response(util.success(self,serializer.data))
            else:
                return Response(util.error(self,"No Data Found"))
        except Exception as e:
            return Response(util.error(self,str(e)))

def get_lat_long(address, city, state):
    try:
        full_address = f"{address}, {city}, {state}"
        geolocator = Nominatim(user_agent="MLS-tutorlatlong")  # Specify a unique user agent

        # try:
        location = geolocator.geocode(full_address, timeout=10)
        if location is None:
            addr2 = f"{city}, {state}"
            loc2 = geolocator.geocode(addr2, timeout=10)
            
            if loc2 is None:
                print("Unable to geocode the address.")
                return None
            else:
                latitude = loc2.latitude
                longitude = loc2.longitude
                return latitude,longitude
        else:
            latitude = location.latitude
            longitude = location.longitude
            return latitude,longitude
    except GeocoderTimedOut:
        return None

class PropertyDetail(APIView):
    def post(self,request,format=None):
        try:
            propertylistingtype=request.POST['property_listing_type']
            if Property_Listing_Type.objects.filter(id=propertylistingtype):
                propertylistingtypeobj=Property_Listing_Type.objects.get(id=propertylistingtype)
                propetylistobj=Propertylisting_type.objects.get(id=propertylistingtypeobj.type_of_listing.id)   

            else:
                propetylistobj=None
                propertylistingtypeobj=None
                
            propertytitle=request.POST.get('propertytitle') 
            propertydescription=request.POST.get('propertydescription')
            propertymainimage=request.FILES.getlist('propertymainimage')
            propertymainfloarplan=request.FILES.get('propertymainfloarplan')

            propertymaincategoryid=request.POST.get('propertymaincategoryid')
            if Property_Main_Category.objects.filter(id=propertymaincategoryid):
                propertymaincategoryobj=Property_Main_Category.objects.get(id=propertymaincategoryid)
            else:
                propertymaincategoryobj = None

            propertysubcategoryid= request.POST.get('propertysubcategoryid')   
            if Property_Sub_Category.objects.filter(id=propertysubcategoryid):
                propertysubcategoryobj=Property_Sub_Category.objects.get(id=propertysubcategoryid)
            else:
                propertysubcategoryobj=None

            propertytypeid=request.POST.get('propertytypeid')
            if Property_Type.objects.filter(id=propertytypeid):
                propertytypeobj=Property_Type.objects.get(id=propertytypeid)
            else:
                propertytypeobj=None

            propertycityid=request.POST.get('propertycity')
            if propertycityid != None:
                if CityMaster.objects.filter(id=propertycityid):
                    propercityobj=CityMaster.objects.get(id=propertycityid)
            else:
                propercityobj=None
            
            propertystateid=request.POST.get('propertystate')
            if propertystateid != "null":
                if StateMaster.objects.filter(id=propertystateid):
                    statemasterobj=StateMaster.objects.get(id=propertystateid)
            else:
                statemasterobj=None

            

            propertyareaid=request.POST.get('propertyarea')
            if propertyareaid != "null":
                if AreaMaster.objects.filter(id=propertyareaid):
                    propertyareaid=AreaMaster.objects.get(id=propertyareaid)
            else:
                propertyareaid=None   

            propertyzipid=request.POST.get('property_zip')

            fees=request.POST.get('fees')
            SellerAgency=request.POST.get('SellerAgency')
            BuyerAgency=request.POST.get('BuyerAgency')

            propertyaddress1=request.POST.get('property_address_1')
            appartment= request.POST.get('appartment')
            propertystartdateid=request.POST.get('property_listing_start_date')
            propertyenddateid=request.POST.get('property_listing_end_date')

            propertyterms = request.POST.get('property_terms')
            propertyoffer = request.POST.get('property_offer')
            ispropertyfee = request.POST.get('is_property_fee')
            propertylistingamount = request.POST.get('property_listing_amount')
            # createddatetime= request.POST.get('created_date_time')
            # createddate = request.POST.get('created_date')
            # createdtime = request.POST.get('created_time')
            # notsurepetfrendly=request.POST.get('notsurepetfrendly')
            # petfrendly_id_list=request.POST.getlist('petfrendly_id_list')
            # main_category_id_list=request.POST.getlist('main_category_id_list')
            is_property_exclusive=request.POST.get('is_property_exclusive')

            userid = request.POST.get('userid')
            propertypetfriendly=request.POST.get('property_pet_friendly')
            min30shows=request.POST.get('min_30_shows')
            NosurePetallowed=request.POST.get('No_sure_Pet_allowed')




            if (request.POST.get('Bedrooms')):
                bedrooms=int(request.POST.get('Bedrooms'))
            else:
                bedrooms= None
            
            if (request.POST.get('Bathrooms')):
                bathrooms=int(request.POST.get('Bathrooms'))
            else:
                bathrooms = None
            
            if (request.POST.get('Square_sqft')):
                squaresqft=int(request.POST.get('Square_sqft'))
            else:
                squaresqft = None
            
            if (request.POST.get('property_cost_per_sq')):
                property_cost_per_sq=int(request.POST.get('property_cost_per_sq'))
            else:
                property_cost_per_sq = None

            if (request.POST.get('Exterior_Sqft')):
                exteriorsqft=int(request.POST.get('Exterior_Sqft'))
            else:
                exteriorsqft = None

            if (request.POST.get('Maintence_fee')):
                maintencefee=int(request.POST.get('Maintence_fee'))
            else:
                maintencefee = None

            if (request.POST.get('Real_Estate_Tax')):
                realestatetax=int(request.POST.get('Real_Estate_Tax'))
            else:
                realestatetax = None

            if (request.POST.get('Financing')):
                financing=int(request.POST.get('Financing'))
            else:
                financing = None

            if (request.POST.get('Minimum_Down')):
                minimum_down = int(request.POST.get('Minimum_Down'))
            else:
                minimum_down = None

            if (request.POST.get('Units')):
                units=int(request.POST.get('Units'))
            else:
                units = None

            if (request.POST.get('Rooms')):
                rooms=int(request.POST.get('Rooms'))
            else:
                rooms = None

            if (request.POST.get('Block')):
                block=int(request.POST.get('Block'))
            else:
                block = None

            if (request.POST.get('Lot')):
                lot=int(request.POST.get('Lot'))
            else:
                lot = None

            if (request.POST.get('Zone')):
                zone=int(request.POST.get('Zone'))
            else:
                zone = None

            if (request.POST.get('Building_Sqft')):
                buildingsqft=int(request.POST.get('Building_Sqft'))
            else:
                buildingsqft = None

            if (request.POST.get('Lot_Dimensions')):
                lotdimension=int(request.POST.get('Lot_Dimensions'))
            else:
                lotdimension = None

            if (request.POST.get('Building_Dimension')):
                buildingdimension=int(request.POST.get('Building_Dimension'))
            else:
                buildingdimension = None

            if (request.POST.get('Stories')):
                stories=int(request.POST.get('Stories'))
            else:
                stories = None

            if (request.POST.get('FAR')):
                far=int(request.POST.get('FAR'))
            else:
                far = None

            if (request.POST.get('Assessment')):
                assessment=int(request.POST.get('Assessment'))
            else:
                assessment = None

            if (request.POST.get('Annual_Taxes')):
                annualtaxes=int(request.POST.get('Annual_Taxes'))
            else:
                annualtaxes = None

            if (request.POST.get('Available_Air_Rights')):
                availableairrights=int(request.POST.get('Available_Air_Rights'))
            else:
                availableairrights = None
            
            aminity_list= request.POST.get('aminity')
            # pet_list= request.POST.get('pets')
            
            # monday = request.POST.get('monday')
            # tuesday = request.POST.get('tuesday')
            # wednesday = request.POST.get('wednesday')
            # thursday = request.POST.get("thursday")
            # friday = request.POST.get("friday")
            # saturday = request.POST.get("saturday")
            # sunday = request.POST.get("sunday")

            space_avaliable = request.POST.get('Space_avaliable')

            open_house = request.POST.get('Open_House')

            mondayopenhouse = request.POST.get('monday_open_house')
            tuesdayopenhouse = request.POST.get('tuesday_open_house')
            wednesdayopenhouse = request.POST.get('wednesday_open_house')
            thursdayopenhouse = request.POST.get("thursday_open_house")
            fridayopenhouse = request.POST.get("friday_open_house")
            saturdayopenhouse = request.POST.get("saturday_open_house")
            sundayopenhouse = request.POST.get("sunday_open_house")

            agentuserprofile = request.POST.get('agentuserprofileid')

            latitude,longitude=get_lat_long(propertyaddress1,propercityobj.city_name,statemasterobj.state_name)
            

            if userid != None and propertylistingtypeobj != None and propertytitle != None and propertymainimage != None and propertymaincategoryobj != None and propertyaddress1 != None and is_property_exclusive != None:
                user, usertype, userprofile=get_user_usertype_userprofile(request, userid)
                if usertype.user_type==2 or usertype.user_type==3 or usertype.user_type==4 or usertype.user_type==5 or usertype.user_type==6:
                    if userprofile:
                        if userprofile.listing_count < 300:
                            propertydetailobj=Property_Detail.objects.create(
                                propertylisting_type=propertylistingtypeobj,
                                property_listing_type = propetylistobj,
                                property_main_category=propertymaincategoryobj,
                                property_sub_category = propertysubcategoryobj ,
                                property_type = propertytypeobj,
                                property_main_image = propertymainimage[0] ,property_main_floor_plan = propertymainfloarplan ,propert_description = propertydescription,property_title = propertytitle,property_address_1= propertyaddress1, property_city = propercityobj , property_area=propertyareaid,property_state = statemasterobj ,property_zip = propertyzipid,   property_terms = propertyterms ,property_offer = propertyoffer , is_property_fee = ispropertyfee ,property_listing_amount = propertylistingamount, user_profile = userprofile , property_pet_friendly = propertypetfriendly ,min_30_shows = min30shows, open_house = open_house ,No_sure_Pet_allowed = NosurePetallowed ,Bedrooms = bedrooms , Bathrooms = bathrooms ,Square_sqft = squaresqft ,property_cost_per_sq=property_cost_per_sq,Exterior_Sqft = exteriorsqft ,Maintence_fee = maintencefee ,Real_Estate_Tax = realestatetax , Financing = financing, Minimum_Down=minimum_down ,Units = units ,Rooms = rooms ,Block = block ,Lot = lot ,Zone = zone , Building_Sqft = buildingsqft , Lot_Dimensions = lotdimension ,Building_Dimension = buildingdimension ,Stories = stories ,FAR = far ,Assessment = assessment ,Annual_Taxes = annualtaxes ,Available_Air_Rights = availableairrights, Apt=appartment, is_property_exclusive=is_property_exclusive,fees=fees,latitude=latitude, longitude=longitude,SellerAgency = SellerAgency, BuyerAgency = BuyerAgency)
                            #  created_date=createddate,created_time=createdtime,
                            userprofile.listing_count = Property_Detail.objects.filter(user_profile = userprofile).count()
                            userprofile.save()

                            # # print(propertydetailobj.is_property_exclusive)

                            if propertydetailobj.is_property_exclusive == "1":
                                propertylistingeventobj=Property_listing_event.objects.create(property_details=propertydetailobj, property_listing_start_date=propertystartdateid, property_listing_end_date=propertyenddateid)
                            else:
                                datetime_obj = datetime.strptime(propertystartdateid, '%Y-%m-%d')
                                futuredate =  datetime_obj + timedelta(days=21)
                                propertylistingeventobj=Property_listing_event.objects.create(property_details=propertydetailobj, property_listing_start_date=propertystartdateid, property_listing_end_date = futuredate)

                            if aminity_list is not None:
                                data=json.loads(aminity_list)
                                if Amenities_Master.objects.filter(id__in=data):
                                    amenitiesobj = Amenities_Master.objects.filter(id__in=data)

                                    for i in amenitiesobj:
                                        amenitiesobj1 = Amenities_Master.objects.get(id=i.id)
                                        Property_Amenities.objects.create(amenites_master=amenitiesobj1,property_details=propertydetailobj,amenities_value=amenitiesobj1.amenities_name)

                            # if pet_list is not None:
                            #     try:
                            #         data=json.loads(pet_list)
                            #         if PetMaster.objects.filter(id__in=data):
                            #             petobj = PetMaster.objects.filter(id__in=data)
                            #             for i in petobj:
                            #                 petmasterobj=PetMaster.objects.get(id=i.id)
                            #                 PetProperty.objects.create(pet_master=petmasterobj,property_details=propertydetailobj)
                            #     except:
                            #         pass
                            if agentuserprofile is not None:
                                data1=json.loads(agentuserprofile)
                                if UserProfile.objects.filter(id__in=data1):
                                    userobj = UserProfile.objects.filter(id__in=data1)
                                    for j in userobj:
                                        userobj1 = UserProfile.objects.get(id=j.id)
                                        teamproperty = TeamProperty.objects.create(userprofile_id = userobj1, propertydetail_id = propertydetailobj)

                            if space_avaliable is not None:
                                data2 = json.loads(space_avaliable)
                                for i in data2:
                                    if  i["space"] != "" and i["size"] != "" and i["term"] != "" and i["rate"] != "" and i["type"] != "":
                                        Property_Space_Availabilityobj = Property_Space_Availability.objects.create(
                                            Property = propertydetailobj, space = i["space"], size = i["size"], term = i["term"], rate = i["rate"], type = i["type"],
                                        )

                            # if open_house is not None:
                            #     data3 = json.loads(open_house)
                            #     for data3 in data3:
                            #         if data3["day"] != "" and data3["start_time"] != "" and data3["end_time"] != "":
                            #             openhouseobj = OpenHouseProperty.objects.create(
                            #                 Property = propertydetailobj, Day = data3["day"], start_time = data3["start_time"], end_time = data3["end_time"]
                            #             )

                            open_house_obj = OpenHouseProperty.objects.create(
                                Monday = json.loads(mondayopenhouse),
                                Tuesday = json.loads(tuesdayopenhouse),
                                Wednesday = json.loads(wednesdayopenhouse),
                                Thursday = json.loads(thursdayopenhouse),
                                Friday = json.loads(fridayopenhouse),
                                Saturday = json.loads(saturdayopenhouse),
                                Sunday = json.loads(sundayopenhouse),
                                property_details = propertydetailobj
                            )

                            # json.loads(area_id)
                            # min30obj = Property30minshow.objects.create(
                            #     Monday = json.loads(monday),
                            #     Tuesday = json.loads(tuesday),
                            #     Wednesday = json.loads(wednesday),
                            #     Thursday = json.loads(thursday),
                            #     Friday = json.loads(friday),
                            #     Saturday = json.loads(saturday),
                            #     Sunday = json.loads(sunday),
                            #     property_details = propertydetailobj
                            # )

                            if propertydetailobj.min_30_shows:
                                min30obj = min_30.objects.filter(userprofile = userprofile).last()
                                if min30obj:
                                    min30obj_id = Property30minshow.objects.create(
                                        Monday = min30obj.Monday,
                                        Tuesday = min30obj.Tuesday,
                                        Wednesday = min30obj.Wednesday,
                                        Thursday = min30obj.Thursday,
                                        Friday = min30obj.Friday,
                                        Saturday = min30obj.Saturday,
                                        Sunday = min30obj.Sunday,
                                        property_details = propertydetailobj
                                    )

                            remaning_image = propertymainimage[1:]
                            if remaning_image is not None:
                                for i in remaning_image:
                                    imageobj = Property_Image.objects.create(
                                        property_detail_id=propertydetailobj, property_image = i
                                    )

                            return Response(util.success(self,['success',{"count":userprofile.listing_count}]))
                        else:
                            return Response(util.error(self, "Sorry, But Your Listing Are Full"))
                    else:
                        return Response(util.error(self,'Please Create Your Profile First!'))
                else:
                    return Response(util.error(self,'Not a Valid user to create property Details'))
            else:
                return Response(util.error(self,'userid, property_listing_type, propertytitle, propertymainimage, propertymaincategoryid, property_listing_start_date, property_listing_end_date, property_address_1, is_property_exclusive is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))

    def put(self, request, format=None, id=None):
        try:
            if id is not None:
                Propertydetailobj=Property_Detail.objects.get(id=id)
                propertylistingtype=request.POST.get('property_listing_type')
                propertylistingtypeobj=Property_Listing_Type.objects.get(id=propertylistingtype)
                propetylistobj=Propertylisting_type.objects.get(id=propertylistingtypeobj.type_of_listing.id)
                Propertydetailobj.property_listing_type = propetylistobj
                Propertydetailobj.propertylisting_type=propertylistingtypeobj
                Propertydetailobj.property_title = request.POST.get('propertytitle')
                Propertydetailobj.propert_description = request.POST.get('propertydescription')
                property_sub_category = request.POST.get('propertysubcategoryid')

                if property_sub_category != "null":
                    if Property_Sub_Category.objects.filter(id = property_sub_category):
                        Propertydetailobj.property_sub_category = Property_Sub_Category.objects.get(id = property_sub_category)

                property_main_category = request.POST.get('propertymaincategoryid')
                if Property_Main_Category.objects.filter(id = property_main_category):
                    Propertydetailobj.property_main_category = Property_Main_Category.objects.get(id = property_main_category)

                Propertydetailobj.property_address_1 = request.POST.get('property_address_1')

                property_city = request.POST.get('propertycity')
                if property_city != "null":
                    if CityMaster.objects.filter(id = property_city):
                        Propertydetailobj.property_city = CityMaster.objects.get(id = property_city)

                property_state = request.POST.get('propertystate')
                if property_state != "null":
                    if StateMaster.objects.filter(id = property_state):
                        Propertydetailobj.property_state = StateMaster.objects.get(id = property_state)

                property_area = request.POST.get('propertyarea')
                if property_area != "null":
                    if AreaMaster.objects.filter(id = property_area):
                        Propertydetailobj.property_area = AreaMaster.objects.get(id = property_area)

                latitude,longitude=get_lat_long(Propertydetailobj.property_address_1,Propertydetailobj.property_city.city_name,Propertydetailobj.property_state.state_name)

                # location = Propertydetailobj.property_address_1+', '+Propertydetailobj.property_city.city_name+', '+Propertydetailobj.property_state.state_name
                # geolocator = Nominatim(user_agent="hiii")
                # location_lat_log = geolocator.geocode(location)
                Propertydetailobj.latitude=latitude
                Propertydetailobj.longitude=longitude

                Propertydetailobj.property_zip = request.POST.get('property_zip')
                Propertydetailobj.property_terms = request.POST.get('property_terms')
                Propertydetailobj.property_offer = request.POST.get('property_offer')
                Propertydetailobj.is_property_fee = request.POST.get('is_property_fee')
                Propertydetailobj.property_listing_amount = request.POST.get('property_listing_amount')
                Propertydetailobj.Apt = request.POST.get('appartment')
                Propertydetailobj.is_property_exclusive = request.POST.get('is_property_exclusive')
                Propertydetailobj.property_pet_friendly = request.POST.get('property_pet_friendly')
                Propertydetailobj.min_30_shows = request.POST.get('min_30_shows')
                Propertydetailobj.fees = request.POST.get('fees')
                Propertydetailobj.SellerAgency = request.POST.get('SellerAgency')
                Propertydetailobj.BuyerAgency = request.POST.get('BuyerAgency')
                Propertydetailobj.open_house = request.POST.get('Open_House')

                if (request.POST.get('Bedrooms')):
                    Propertydetailobj.Bedrooms = request.POST.get('Bedrooms')
                else:
                    Propertydetailobj.Bedrooms = None

                if (request.POST.get('Bathrooms')):
                    Propertydetailobj.Bathrooms = request.POST.get('Bathrooms')
                else:
                    Propertydetailobj.Bathrooms = None

                if (request.POST.get('Square_sqft')):
                    Propertydetailobj.Square_sqft = request.POST.get('Square_sqft')
                else:
                    Propertydetailobj.Square_sqft = None

                if (request.POST.get('Exterior_Sqft')):
                    Propertydetailobj.Exterior_Sqft = request.POST.get('Exterior_Sqft')
                else:
                    Propertydetailobj.Exterior_Sqft = None
                if(request.POST.get('Maintence_fee')):
                    Propertydetailobj.Maintence_fee = request.POST.get('Maintence_fee')
                else:
                    Propertydetailobj.Maintence_fee = None

                if(request.POST.get('Real_Estate_Tax')):
                    Propertydetailobj.Real_Estate_Tax = request.POST.get('Real_Estate_Tax')
                else:
                    Propertydetailobj.Real_Estate_Tax = None

                if(request.POST.get('Financing')):
                    Propertydetailobj.Financing = request.POST.get('Financing')
                else:
                    Propertydetailobj.Financing = None

                if(request.POST.get('Minimum_Down')):
                    Propertydetailobj.Minimum_Down = request.POST.get('Minimum_Down')
                else:
                    Propertydetailobj.Minimum_Down = None

                if(request.POST.get('created_date')):
                    Propertydetailobj.created_date = request.POST.get('created_date')
                else:
                    Propertydetailobj.created_date = None

                if(request.POST.get('created_time')):
                    Propertydetailobj.created_time = request.POST.get('created_time')
                else:
                    Propertydetailobj.created_time = None

                if(request.POST.get('No_sure_Pet_allowed')):
                    Propertydetailobj.No_sure_Pet_allowed = request.POST.get('No_sure_Pet_allowed')
                else:
                    Propertydetailobj.No_sure_Pet_allowed = None

                if(request.POST.get('Units')):
                    Propertydetailobj.Units = request.POST.get('Units')
                else:
                    Propertydetailobj.Units = None

                if(request.POST.get('Rooms')):
                    Propertydetailobj.Rooms = request.POST.get('Rooms')
                else:
                    Propertydetailobj.Rooms = None

                if(request.POST.get('Block')):
                    Propertydetailobj.Block = request.POST.get('Block')
                else:
                    Propertydetailobj.Block = None

                if(request.POST.get('Lot')):
                    Propertydetailobj.Lot = request.POST.get('Lot')
                else:
                    Propertydetailobj.Lot = None

                if(request.POST.get('Zone')):
                    Propertydetailobj.Zone = request.POST.get('Zone')
                else:
                    Propertydetailobj.Zone = None

                if(request.POST.get('Building_Sqft')):
                    Propertydetailobj.Building_Sqft = request.POST.get('Building_Sqft')
                else:
                    Propertydetailobj.Building_Sqft = None

                if(request.POST.get('Lot_Dimensions')):
                    Propertydetailobj.Lot_Dimensions = request.POST.get('Lot_Dimensions')
                else:
                    Propertydetailobj.Lot_Dimensions = None

                if(request.POST.get('Building_Dimension')):
                    Propertydetailobj.Building_Dimension = request.POST.get('Building_Dimension')
                else:
                    Propertydetailobj.Building_Dimension = None

                if(request.POST.get('Stories')):
                    Propertydetailobj.Stories = request.POST.get('Stories')
                else:
                    Propertydetailobj.Stories = None

                if(request.POST.get('FAR')):
                    Propertydetailobj.FAR = request.POST.get('FAR')
                else:
                    Propertydetailobj.FAR = None

                if(request.POST.get('Assessment')):
                    Propertydetailobj.Assessment = request.POST.get('Assessment')
                else:
                    Propertydetailobj.Assessment = None

                if(request.POST.get('Annual_Taxes')):
                    Propertydetailobj.Annual_Taxes = request.POST.get('Annual_Taxes')
                else:
                    Propertydetailobj.Annual_Taxes = None

                if(request.POST.get('Available_Air_Rights')):
                    Propertydetailobj.Available_Air_Rights = request.POST.get('Available_Air_Rights')
                else:
                    Propertydetailobj.Available_Air_Rights = None



                property_main_image = request.FILES.getlist('propertymainimage')
                if property_main_image:
                    Propertydetailobj.property_main_image = property_main_image[0]
                else:
                    pass

                property_floor_plan = request.FILES.get('propertymainfloarplan')
                if property_floor_plan:
                    Propertydetailobj.property_main_floor_plan = property_floor_plan
                else:
                    pass



                Propertydetailobj.save()

                # multiple Images
                remaning_image = property_main_image[1:]
                if remaning_image:
                    imageobj = Property_Image.objects.filter(property_detail_id=Propertydetailobj)
                    for i in imageobj:
                        i.delete()
                    for remaning_image in remaning_image:
                        imageobj = Property_Image.objects.create(
                                    property_detail_id=Propertydetailobj, property_image = remaning_image
                                )
                else:
                    pass

                # Exclusive or open data
                property_listing_start_date = request.POST.get('property_listing_start_date')
                property_listing_end_date = request.POST.get('property_listing_end_date')

                propertylistingeventobj=Property_listing_event.objects.get(property_details=Propertydetailobj)
                if Propertydetailobj.is_property_exclusive == 1:
                    propertylistingeventobj.property_listing_start_date=property_listing_start_date, propertylistingeventobj.property_listing_end_date=property_listing_end_date
                else:
                    propertylistingeventobj.property_listing_start_date=property_listing_start_date

                propertylistingeventobj.save()

                # pet Master
                property_pets = request.POST.get('pets')
                if property_pets:
                    try:
                        data=json.loads(property_pets)
                        if PetMaster.objects.filter(id__in=data):
                            petobj = PetMaster.objects.filter(id__in=data)
                            for i in petobj:
                                petmasterobj=PetMaster.objects.get(id=i.id)
                                if PetProperty.objects.filter(pet_master=petmasterobj,property_details=Propertydetailobj):
                                    pass
                                PetProperty.objects.create(pet_master=petmasterobj,property_details=Propertydetailobj)
                    except:
                        pass

                # Amenities
                property_amenities = request.POST.get('aminity')
                if property_amenities:
                    try:
                        data=json.loads(property_amenities)
                        if Amenities_Master.objects.filter(id__in=data):
                            amenitiesobj = Amenities_Master.objects.filter(id__in=data)
                            for i in amenitiesobj:
                                amenitiesobj1 = Amenities_Master.objects.get(id=i.id)
                                if Property_Amenities.objects.filter(amenites_master=amenitiesobj1,property_details=Propertydetailobj):
                                    propetyamentiesobj = Property_Amenities.objects.filter(amenites_master=amenitiesobj1,property_details=Propertydetailobj)
                                    for i in propetyamentiesobj:
                                        i.delete()
                                    Property_Amenities.objects.create(amenites_master=amenitiesobj1,property_details=Propertydetailobj,amenities_value=amenitiesobj1.amenities_name)
                                else:
                                    Property_Amenities.objects.create(amenites_master=amenitiesobj1,property_details=Propertydetailobj,amenities_value=amenitiesobj1.amenities_name)
                    except:
                        pass

                # Team Memeber
                agentuserprofile = request.POST.get('agentuserprofileid')
                if agentuserprofile:
                    try:
                        data1=json.loads(agentuserprofile)
                        team = TeamProperty.objects.filter(propertydetail_id = Propertydetailobj)
                        for i in team:
                            i.delete()
                        if UserProfile.objects.filter(id__in=data1):
                            userobj = UserProfile.objects.filter(id__in=data1)
                            for j in userobj:
                                userobj1 = UserProfile.objects.get(id=j.id)
                                teamobj = TeamProperty.objects.create(userprofile_id = userobj1, propertydetail_id = Propertydetailobj)
                    except:
                        pass

                # Space Avaliable
                property_space_avaliable = request.POST.get('Space_avaliable')
                if property_space_avaliable:
                    try:
                        data2 = json.loads(property_space_avaliable)
                        for i in data2:
                            if  i["space"] != "" and i["size"] != "" and i["term"] != "" and i["rate"] != "" and i["type"] != "":
                                if Property_Space_Availability.objects.filter(
                                            Property = Propertydetailobj, space = i["space"], size = i["size"], term = i["term"], rate = i["rate"], type = i["type"],
                                        ):
                                    pass
                                else:
                                    Property_Space_Availability.objects.create(
                                            Property = Propertydetailobj, space = i["space"], size = i["size"], term = i["term"], rate = i["rate"], type = i["type"],
                                        )
                    except:
                        pass

                # OpenHouse
                mondayopenhouse = request.POST.get('monday_open_house')
                tuesdayopenhouse = request.POST.get('tuesday_open_house')
                wednesdayopenhouse = request.POST.get('wednesday_open_house')
                thursdayopenhouse = request.POST.get("thursday_open_house")
                fridayopenhouse = request.POST.get("friday_open_house")
                saturdayopenhouse = request.POST.get("saturday_open_house")
                sundayopenhouse = request.POST.get("sunday_open_house")

                open_house_obj = OpenHouseProperty.objects.create(
                    Monday = json.loads(mondayopenhouse),
                    Tuesday = json.loads(tuesdayopenhouse),
                    Wednesday = json.loads(wednesdayopenhouse),
                    Thursday = json.loads(thursdayopenhouse),
                    Friday = json.loads(fridayopenhouse),
                    Saturday = json.loads(saturdayopenhouse),
                    Sunday = json.loads(sundayopenhouse),
                    property_details = Propertydetailobj
                )

                # min_30_show
                property_sunday = request.POST.get('sunday')
                property_monday = request.POST.get('monday')
                property_tuesday = request.POST.get('tuesday')
                property_wednesday = request.POST.get('wednesday')
                property_thursday = request.POST.get('thursday')
                property_friday = request.POST.get('friday')
                property_saturday = request.POST.get('saturday')

                min30obj = Property30minshow.objects.create(
                    Monday = json.loads(property_monday),
                    Tuesday = json.loads(property_tuesday),
                    Wednesday = json.loads(property_wednesday),
                    Thursday = json.loads(property_thursday),
                    Friday = json.loads(property_friday),
                    Saturday = json.loads(property_saturday),
                    Sunday = json.loads(property_sunday),
                    property_details = Propertydetailobj
                )
                return Response(util.success(self, "Successfully Updated"))
            else:
                return Response(util.error(self, "Propery Detail Not Found"))
        except Exception as e:
            return Response(util.error(self,str(e)))

    def delete(self, request, format=None):
        try:
            data =json.loads(request.body)
            # data=request.data
            if 'userid' in data and 'Property_Detail_id' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['userid'])
                # if usertype.user_type==2 and usertype.user_type==4 and usertype.user_type==5:
                if usertype.user_type==2 or usertype.user_type==4 or usertype.user_type==5:
                    if Property_Detail.objects.filter(id=data['Property_Detail_id']):
                        property_detail_obj=Property_Detail.objects.get(id=data['Property_Detail_id'])
                        if property_detail_obj.user_profile.id == userprofile.id:
                            property_detail_obj.delete()
                            userprofile.listing_count =- 1
                            userprofile.save()
                            return Response(util.success(self,'Property Detail deleted Successfully'))
                        else:
                            return Response(util.error(self,'Not Valid User to Delete Property'))
                    else:
                        return Response(util.error(self,'Not a Valid Property detail Id'))
                else:
                    return Response(util.error(self,'Not Valid User to Delete Property'))
            else:
                    return Response(util.error(self,'userid and Property_Detail_id Needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

    def get(self,request, format=None,slug=None):
        try:
            if slug==None:
                productdetailobj=Property_Detail.objects.all()
                serializer=PropertyDetailSerializer(productdetailobj, many=True)
            else:
                if Property_Detail.objects.filter(slug=slug):
                    productdetailobj=Property_Detail.objects.get(slug=slug)
                    serializer=GetPropertyDetailSerializer(productdetailobj)
                else:
                    return Response(util.error(self,'Product Detail Not Found'))
            if serializer.data:
                return Response(util.success(self,serializer.data))
            else:
                return Response(util.error(self,"No Data Found"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class Update_is_property_open(APIView):
    def put(self,request, format=None):
        try:
            data = request.data
            if 'userid' in data and 'propertyid' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['userid'])
                if usertype.user_type==2 or usertype.user_type==3 or usertype.user_type==4 or usertype.user_type==5:
                    if userprofile:
                        # property=json.loads(data['propertyid'])
                        if Property_Detail.objects.filter(user_profile=userprofile,id__in=data['propertyid']):
                            propertyobj=Property_Detail.objects.filter(user_profile=userprofile, id__in=data['propertyid'])
                            for i in propertyobj:
                                if i.is_property_open == False:
                                    i.is_property_open = True
                                else:
                                    i.is_property_open = False
                                i.save()
                                # print(i.is_property_open)
                            return Response(util.success(self, 'Property Detail Update Successfully'))
                        else:
                            return Response(util.error(self, 'Detail not found'))
                    else:
                        return Response(util.error(self, 'userprofile not found'))
                else:
                    return Response(util.error(self,'Not Valid User to update Property'))
            else:
                return Response(util.error(self, 'userid, propertyid is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

    def get(self, request, format=None, id=None):
        try:
            if id is not None:
                user,usertype,userprofile=get_user_usertype_userprofile(request,id)
                if usertype.user_type==2 or usertype.user_type==3 or usertype.user_type==4 or usertype.user_type==5 or usertype.user_type==6:
                    if userprofile:
                        propertyobj=Property_Detail.objects.filter(user_profile=userprofile)
                        serializer = PropertyDetailSerializer(propertyobj, many=True)
                        if serializer:
                            return Response(util.success(self, serializer.data))
                        else:
                            return Response(util.error(self, 'no data found'))
                    else:
                        return Response(util.error(self, 'userprofile not found'))
                else:
                    return Response(util.error(self,'Not Valid User to update Property'))
            else:
                return Response(util.error(self,'User id not found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class DeleteProperty(APIView):
    def post(self, request, format = None):
        try:
            data = request.data
            user,usertype,userprofile=get_user_usertype_userprofile(request,data['userid'])
            if user:
                if 'propertyid' in data:
                    propertyobj = Property_Detail.objects.filter(id__in=data['propertyid'])
                    for i in propertyobj:
                        propertyid = Property_Detail.objects.get(id=i.id)
                        propertyid.delete()
                        listing = propertyid.user_profile.listing_count
                        listingid = (listing - 1)
                        userprofile.listing_count = listingid
                        userprofile.save()
                    return Response(util.success(self,'Property deleted successfully'))
                else:
                    return Response(util.error(self, 'propertyid is needed'))
            else:
                return Response(util.error(self,'Not Valid User'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class Update_is_property_expired(APIView):
    def put(self,request, format=None):
        try:
            data = request.data
            if 'userid' in data and 'propertyid' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['userid'])
                if usertype.user_type==2 or usertype.user_type==3 or usertype.user_type==4 or usertype.user_type==5:
                    if userprofile:
                        # property=json.loads(data['propertyid'])
                        if Property_Detail.objects.filter(user_profile=userprofile,id__in=data['propertyid']):
                            propertyobj=Property_Detail.objects.filter(user_profile=userprofile, id__in=data['propertyid'])
                            for i in propertyobj:
                                if i.is_property_expired == False:
                                    i.is_property_expired = True
                                else:
                                    propertyevnetobj = Property_listing_event.objects.filter(property_details = i)
                                    today = datetime.now(timezone.utc)
                                    for j in propertyevnetobj:
                                        if j.property_listing_end_date is None:
                                            j.property_listing_start_date = today
                                        else:
                                            start_date = j.property_listing_start_date
                                            end_date = j.property_listing_end_date
                                            minusday = end_date - start_date
                                            futuredate = today + timedelta(days=minusday.days)
                                            j.property_listing_start_date = today
                                            j.property_listing_end_date = futuredate
                                        j.save()
                                    i.is_property_expired = False
                                i.save()
                            return Response(util.success(self, 'Property Detail Update Successfully'))
                        else:
                            return Response(util.error(self, 'Detail not found'))
                    else:
                        return Response(util.error(self, 'userprofile not found'))
                else:
                    return Response(util.error(self,'Not Valid User to update Property'))
            else:
                return Response(util.error(self, 'userid, propertyid is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class ExpiredListingProperty(APIView):
    def get(self, request, format=None, id=None):
        try:
            if id is not None:
                user,usertype,userprofile=get_user_usertype_userprofile(request,id)
                if usertype.user_type==2 or usertype.user_type==3 or usertype.user_type==4 or usertype.user_type==5:
                    if userprofile:
                        if Property_Detail.objects.filter(user_profile=userprofile.id):
                            propertyobj=Property_Detail.objects.filter(user_profile=userprofile).filter(is_property_expired=True, is_property_open = True)
                            teamproperty = TeamProperty.objects.filter(userprofile_id=userprofile)

                            serializer=PropertyDetailSerializer(propertyobj, many=True)

                            serializer1=TeamPropertySerializer(teamproperty, many = True)

                            if serializer.data:
                                if serializer1.data:
                                    return Response(util.success(self,[serializer.data,serializer1.data]))
                                else:
                                    return Response(util.success(self,serializer.data))
                            else:
                                return Response(util.error(self, 'No Data Found'))
                        else:
                            return Response(util.error(self, 'Detail not found'))
                    else:
                        return Response(util.error(self, 'userprofile not found'))
                else:
                    return Response(util.error(self,'Not Valid User to update Property'))
            else:
                return Response(util.error(self, "id is required"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class UnExpiredListingProperty(APIView):
    def post(self, request, format=None):
        try:
            if request.data['user_id'] is not None and request.data['date'] is not None:
                user,usertype,userprofile=get_user_usertype_userprofile(request,request.data['user_id'])
                if usertype.user_type==2 or usertype.user_type==3 or usertype.user_type==4 or usertype.user_type==5:
                    if userprofile:
                        today = datetime.strptime(request.data['date'], "%Y-%m-%d")
                        propertyobj=Property_Detail.objects.filter( is_property_expired=False, is_property_open = True,  user_profile = userprofile).values_list('id', flat=True)
                        if propertyobj is None:
                            return Response(util.error(self, 'Detail not found'))
                        teamproperty = TeamProperty.objects.filter(userprofile_id=userprofile)
                        propertyevnetobj = Property_listing_event.objects.filter(property_details__in = propertyobj)
                        for i in propertyevnetobj:
                            end_date = i.property_listing_end_date
                            if end_date is not None:
                                if end_date.date() <= today.date():
                                    propertyid = Property_Detail.objects.get(id = i.property_details.id)
                                    propertyid.is_property_expired = True
                                    propertyid.save()
                        
                        propertyidobj=Property_Detail.objects.filter(is_property_expired=False, is_property_open=True, user_profile = userprofile).order_by('-pk')
                        serializer=PropertyDetailSerializer(propertyidobj, context={'virtual_office_id':request.data['virtual_office_id'],"user":request.user}, many=True)
                        serializer1=TeamPropertySerializer(teamproperty, many = True)
                        
                        if serializer.data:
                            if serializer1.data:
                                return Response(util.success(self,[serializer.data,serializer1.data]))
                            else:
                                return Response(util.success(self,serializer.data))
                        else:
                            return Response(util.error(self, 'No Data Found'))
                         
                            
                    else:
                        return Response(util.error(self, 'userprofile not found'))
                else:
                    return Response(util.error(self,'Not Valid User to update Property'))
            else:
                return Response(util.error(self,'user_id, date are required'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class AgentDashboardProperty(APIView):
    def post(self, request, format=None):
        try:
            if request.data['user_id'] is not None and request.data['date'] is not None:
                user,usertype,userprofile=get_user_usertype_userprofile(request,request.data['user_id'])
                if usertype.user_type==2 or usertype.user_type==3 or usertype.user_type==4 or usertype.user_type==5:
                    if userprofile:
                        today = datetime.strptime(request.data['date'], "%Y-%m-%d")
                        propertyobj=Property_Detail.objects.filter( is_property_expired=False, is_property_open = True).values_list('id', flat=True)
                        if propertyobj is None:
                            return Response(util.error(self, 'Detail not found'))
                        teamproperty = TeamProperty.objects.filter(userprofile_id=userprofile)
                        propertyevnetobj = Property_listing_event.objects.filter(property_details__in = propertyobj)
                        for i in propertyevnetobj:
                            end_date = i.property_listing_end_date
                            if end_date is not None:
                                if end_date.date() <= today.date():
                                    propertyid = Property_Detail.objects.get(id = i.property_details.id)
                                    propertyid.is_property_expired = True
                                    propertyid.save()
                        
                        propertyidobj=Property_Detail.objects.filter(is_property_expired=False, is_property_open=True).order_by('-pk')
                        serializer=PropertyDetailSerializer(propertyidobj, context={'virtual_office_id':request.data['virtual_office_id'],"user":request.user}, many=True)
                        serializer1=TeamPropertySerializer(teamproperty, many = True)
                        
                        if serializer.data:
                            if serializer1.data:
                                return Response(util.success(self,[serializer.data,serializer1.data]))
                            else:
                                return Response(util.success(self,serializer.data))
                        else:
                            return Response(util.error(self, 'No Data Found'))
                         
                            
                    else:
                        return Response(util.error(self, 'userprofile not found'))
                else:
                    return Response(util.error(self,'Not Valid User to update Property'))
            else:
                return Response(util.error(self,'user_id, date are required'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class CurrentlistingProperty(APIView):
    def get(self, request, format=None, slug=None):
        try:
            if slug is not None:
                userprofileobj = UserProfile.objects.get(slug = slug)
                user,usertype,userprofile=get_user_usertype_userprofile(request,userprofileobj.user_type.user.id)
                if usertype.user_type==2 or usertype.user_type==3 or usertype.user_type==4 or usertype.user_type==5:
                    if userprofile:
                        if Property_Detail.objects.filter(user_profile=userprofile.id):
                            propertyobj=Property_Detail.objects.filter(user_profile=userprofile,  is_property_expired=False, is_property_open = True)
                            teamproperty = TeamProperty.objects.filter(userprofile_id=userprofile)

                            serializer=PropertyDetailSerializer(propertyobj, many=True)

                            serializer1=TeamPropertySerializer(teamproperty, many = True)
                            
                            if serializer.data:
                                if serializer1.data:
                                    return Response(util.success(self,[serializer.data,serializer1.data]))
                                else:
                                    return Response(util.success(self,serializer.data))
                            else:
                                return Response(util.error(self, 'No Data Found'))
                        else:
                            return Response(util.error(self, 'Detail not found'))
                    else:
                        return Response(util.error(self, 'userprofile not found'))    
                else:
                    return Response(util.error(self,'Not Valid User to update Property'))
            else:
                return Response(util.error(self, 'Slug is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class CloselistingProperty(APIView):
    def get(self, request, format=None, slug = None):
        try:
            if slug is not None:
                userprofileobj = UserProfile.objects.get(slug = slug)
                user,usertype,userprofile=get_user_usertype_userprofile(request, userprofileobj.user_type.user.id)
                if usertype.user_type==2 or usertype.user_type==3 or usertype.user_type==4 or usertype.user_type==5:
                    if userprofile:
                        if Property_Detail.objects.filter(user_profile=userprofile):
                            propertyobj=Property_Detail.objects.filter(user_profile=userprofile).filter(is_property_open=False)
                            teamproperty = TeamProperty.objects.filter(userprofile_id=userprofile)

                            serializer=PropertyDetailSerializer(propertyobj, many=True)

                            serializer1=TeamPropertySerializer(teamproperty, many = True)

                            if serializer.data:
                                if serializer1.data:
                                    return Response(util.success(self,[serializer.data,serializer1.data]))
                                else:
                                    return Response(util.success(self,serializer.data))
                            else:
                                return Response(util.error(self, 'No Data Found'))
                        else:
                            return Response(util.error(self, 'Detail not found'))
                    else:
                        return Response(util.error(self, 'userprofile not found'))    
                else:
                    return Response(util.error(self,'Not Valid User to update Property'))
            else:
                return Response(util.error(self, 'Slug is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class CurrentlistingPropertycount(APIView):
    def get(self, request, format=None, slug=None):
        try:
            if slug is not None:
                userprofileobj = UserProfile.objects.get(slug = slug)
                user,usertype,userprofile=get_user_usertype_userprofile(request, userprofileobj.user_type.user.id)
                if usertype.user_type==2 or usertype.user_type==3 or usertype.user_type==4 or usertype.user_type==5:
                    if userprofile:
                        if Property_Detail.objects.filter(user_profile=userprofile):
                            propertyobj=Property_Detail.objects.filter(user_profile=userprofile,   is_property_open = True).count()
                            if propertyobj != 0:
                                return Response(util.success(self,propertyobj))
                            else:
                                return Response(util.error(self, 'Detail not found'))
                        else:
                            return Response(util.error(self, 'Detail not found'))
                    else:
                        return Response(util.error(self, 'userprofile not found'))    
                else:
                    return Response(util.error(self,'Not Valid User to update Property'))
            else:
                return Response(util.error(self, 'slug is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class CloselistingPropertycount(APIView):
    def get(self, request, format=None, slug=None):
        try:
            if slug is not None:
                userprofileobjid = UserProfile.objects.get(slug = slug)
                user,usertype,userprofile=get_user_usertype_userprofile(request, userprofileobjid.user_type.user.id)
                if usertype.user_type==2 or usertype.user_type==3 or usertype.user_type==4 or usertype.user_type==5:
                    if userprofile:
                        if Property_Detail.objects.filter(user_profile=userprofile):
                            propertyobj=Property_Detail.objects.filter(user_profile=userprofile).filter(is_property_open=False).count()
                            if propertyobj != 0:
                                return Response(util.success(self,propertyobj))
                            else:
                                return Response(util.error(self, 'Detail not found'))
                        else:
                            return Response(util.error(self, 'Detail not found'))
                    else:
                        return Response(util.error(self, 'userprofile not found'))    
                else:
                    return Response(util.error(self,'Not Valid User to update Property'))
            else:
                return Response(util.error(self, 'slug is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class TotallistingPropertycount(APIView):
    def get(self, request, format=None, slug=None):
        try:
            if slug is not None:
                userprofileobjid = UserProfile.objects.get(slug = slug)
                user,usertype,userprofile=get_user_usertype_userprofile(request, userprofileobjid.user_type.user.id)
                if usertype.user_type==2 or usertype.user_type==3 or usertype.user_type==4 or usertype.user_type==5:
                    if userprofile:
                        if Property_Detail.objects.filter(user_profile=userprofile):
                            propertyobj=Property_Detail.objects.filter(user_profile=userprofile).count()
                            if propertyobj != 0:
                                return Response(util.success(self,propertyobj))
                            else:
                                return Response(util.error(self, 'Detail not found'))
                        else:
                            return Response(util.error(self, 'Detail not found'))
                    else:
                        return Response(util.error(self, 'userprofile not found'))    
                else:
                    return Response(util.error(self,'Not Valid User to update Property'))
            else:
                return Response(util.error(self, 'id is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class PropertyAmenities(APIView):
    def post(self,request, format=None,id=None):
        try:
            data =json.loads(request.body)
            if 'userid' in data and 'Property_Detail_id' in data and 'aminity_list' in data and 'created_date' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['userid'])
                if usertype.user_type==2 and usertype.user_type==3 and usertype.user_type==4 and usertype.user_type==5:
                    if Property_Detail.objects.filter(id=data['Property_Detail_id']):
                        propertydetailobj = Property_Detail.objects.get(id=data['Property_Detail_id'])
                    else:
                        propertydetailobj=None

                    if propertydetailobj != None:
                        for key in data['aminity_list']:
                            if Amenities_Master.objects.filter(id=key):
                                amenitiesobj=Amenities_Master.objects.get(id=key)
                                Property_Amenities.objects.create(amenites_master=amenitiesobj,property_details=propertydetailobj,amenities_value=data[key])
                                # return Response({'msg':'Amenities Created Successfully'})
                                return Response(util.success(self,'Amenities Created Successfully'))
                            else:
                                # return Response({'msg':'Amenities Master id is not valid'})
                                return Response(util.error(self,'Amenities Master id is not valid'))
                    else:
                        # return Response({'msg':'Property Detail id is not valid'})
                        return Response(util.error(self,'Property Detail id is not valid'))
                else:
                    # return Response({'msg':'Not a valid user to create Property Amenities'})
                    return Response(util.error(self,'Not a valid user to create Property Amenities'))
            else:
                # return Response({'msg':'userid, Property_Detail_id, aminity_list and created_date Needed'})
                return Response(util.error(self,'userid, Property_Detail_id, aminity_list and created_date Needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

    def put(self, request, format=None):
        try:
            data =json.loads(request.body)
            if 'userid' in data and 'amenites_master_id' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['userid'])
                if usertype.user_type==2 and usertype.user_type==3 and usertype.user_type==4 and usertype.user_type==5:
                    if Property_Amenities.objects.filter(id= data['amenites_master_id']):
                        propertyamenitiesobj=Property_Amenities.objects.get(id= data['amenites_master_id'])
                        if 'property_detail_obj' in data:
                            if Property_Detail.objects.filter(id=data["property_detail_obj"]):
                                propertydetailobj=Property_Detail.objects.get(id= data)
                                propertyamenitiesobj.property_details=propertydetailobj
                            else:
                                # return Response({"msg":"Property Detail Not Found"})
                                return Response(util.error(self,'Property Detail Not Found'))
                        elif 'aminity_value' in data:
                            propertyamenitiesobj.amenities_value=data["aminity_value"]
                        else:
                            # return Response({"msg":"No Field Updated"})
                            return Response(util.error(self,'No Field Updated'))
                    else:
                        # return Response({"msg":"Property Amenities not found"})
                        return Response(util.error(self,'Property Amenities not found'))
                else:
                    # return Response({'msg':"Not a valid user"})
                    return Response(util.error(self,'Not a valid user'))
            else:
                # return Response({'msg':'userid amenites_master_id nedded'})
                return Response(util.error(self,'userid amenites_master_id nedded'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class PropertyListingEvent(APIView):
    def post(self, request, format=None):
        try:
            data =json.loads(request.body)
            if 'userid' in data and 'Property_Detail_id' in data and 'is_property_exclusive' in data and 'property_listing_start_date' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['userid'])
                if usertype.user_type==2 and usertype.user_type==3 and usertype.user_type==4 and usertype.user_type==5:
                    if Property_Detail.objects.filter(id=data["Property_Detail_id"]):
                        propertydetailobj=Property_Detail.objects.filter(id=data["Property_Detail_id"])
                        if data["is_property_exclusive"]:
                            if "property_listing_end_date" in data:
                                Property_listing_event.objects.create(property_details=propertydetailobj,is_property_exclusive=data["is_property_exclusive"],property_listing_start_date=data["property_listing_start_date"],property_listing_end_date=data["property_listing_end_date"])
                                # return Response({'msg':'Property listing event created successfully'})
                                return Response(util.success(self,'Property listing event created successfully'))
                            else:
                                # return Response({'msg': "property_listing_end_date needed"})
                                return Response(util.error(self,'property_listing_end_date needed'))
                        else:
                            if "property_listing_end_date" in data:
                                Property_listing_event.objects.create(property_details=propertydetailobj,is_property_exclusive=data["is_property_exclusive"],property_listing_start_date=data["property_listing_start_date"])
                                # return Response({'msg':'Property listing event created successfully'})
                                return Response(util.success(self,'Property listing event created successfully'))
                    else:
                        # return Response({'msg':'Property Detail Not Found'})
                        return Response(util.error(self,'Property Detail Not Found'))
                else:
                    # return Response({'msg':"Not a valid user"})
                    return Response(util.error(self,'Not a valid user'))
            else:
                # return Response({'msg':'userid, Property_Detail_id, is_property_exclusive, property_listing_start_date nedded'})
                return Response(util.error(self,'userid, Property_Detail_id, is_property_exclusive, property_listing_start_date nedded'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class PropertyImage(APIView):
    def post(self, request, format=None):
        try:
            user_id=request.POST.get('userid')
            property_detail_id=request.POST.get('property_detail_id')
            property_image_type=request.POST.get('property_image_type')
            property_image=request.FILES.get('property_image')
            user,usertype,userprofile=get_user_usertype_userprofile(request,user_id)
            
            if usertype.user_type==2 and usertype.user_type==3 and usertype.user_type==4 and usertype.user_type==5:
                if Property_Detail.objects.filter(id=property_detail_id):
                    propertydetailobj=Property_Detail.objects.get(id=property_detail_id)
                    if property_image_type!=None and property_image!=None:
                        Property_Image.objects.create(property_detail_id=propertydetailobj,property_image_type=property_image_type,property_image=property_image,)
                        # return Response({'msg':"Property Image created successfully"}, status=200)
                        return Response(util.success(self,'Property Image created successfully'))
                    else:
                        # return Response({'msg':'property_image_type and property_image is required '},  status=400)
                        return Response(util.error(self,'property_image_type and property_image is required'))
                else:
                    # return Response({'msg':'Property Detail Not Found'}, status=400)
                    return Response(util.error(self,'Property Detail Not Found'))
            else:
                # return Response({'msg':'Not a valid user'}, status=400)
                return Response(util.error(self,'Not a valid user'))
        except Exception as e:
            return Response(util.error(self,str(e)))
    
    def delete(self, request, format=None):
        try:
            data =json.loads(request.body)
            if 'userid' in data and 'property_image_id' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data["user_id"])
            
                if usertype.user_type==2 and usertype.user_type==3 and usertype.user_type==4 and usertype.user_type==5:
                    if Property_Image.objects.filter(id=data['userid']):
                        propertyimageobj=Property_Image.objects.get(id=data['userid'])
                        propertyimageobj.delete()
                        # return Response({'msg':'Property Image Deleted'},status=200)
                        return Response(util.success(self,'Property Image Deleted'))
                    else:
                        # return Response({'msg':'Property Image id is not valid'},status=400)
                        return Response(util.error(self,'Property Image id is not valid'))
                else:
                    # return Response({'msg':'Not a valid user'},status=400)
                    return Response(util.error(self,'Not a valid user'))
            else:
                # return Response({'msg':'userid and property_image_id id needed'})
                return Response(util.error(self,'userid and property_image_id id needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))
    
    def put(self, request, format=None):
        try:
            data =json.loads(request.body)
            if 'userid' in data and 'property_image_id' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data["user_id"])
                if usertype.user_type==2 and usertype.user_type==3 and usertype.user_type==4 and usertype.user_type==5:
                    if Property_Image.objects.filter(id=data['userid']):
                        propertyimageobj=Property_Image.objects.get(id=data['userid'])
                        if "property_image_type" in data:
                            propertyimageobj.property_image_type=data['property_image_type']
                        if "property_image" in data:
                            propertyimageobj.property_image=data['property_image']
                        if "is_active" in data:
                            propertyimageobj.is_active=data['is_active']
                        else:
                            # return Response({'msg':"No fields to update"})
                            return Response(util.error(self,'No fields to update'))
                        propertyimageobj.save()
                        # return Response({'msg':'Property Image Updated'})
                        return Response(util.success(self,'Property Image Updated'))
                    else:
                        # return Response({'msg':"Property Image Id Not Found"})
                        return Response(util.error(self,'Property Image Id Not Found'))
                else:
                    # return Response({'msg':"Not a valid user"})
                    return Response(util.error(self,'Not a valid user'))
            else:
                # return Response({'msg':"userid and property_image_id is needed"})
                return Response(util.error(self,'userid and property_image_id is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

    def get(self,request, format=None,id=None):
        try:
            data=json.loads(request.body)
            if 'property_detail_id' in data:
                productdetailobj=Property_Image.objects.filter(property_detail_id=data['property_detail_id'])
                serializer=PropertyImageSerializer(productdetailobj, many=True)
            else:

                if id==None:
                    productdetailobj=Property_Image.objects.all()
                    serializer=PropertyImageSerializer(productdetailobj, many=True)
                else:
                    if Property_Detail.objects.filter(id=id):
                        productdetailobj=Property_Detail.objects.get(id=id)
                        serializer=PropertyImageSerializer(productdetailobj)
                    else:
                        # return Response({'msg':'Product Detail Not Found'})
                        return Response(util.error(self,'Product Detail Not Found'))
            # return JsonResponse(serializer.data, safe=False)
            if serializer.data:
                return Response(util.success(self,serializer.data))
            else:
                return Response(util.error(self,'Data Not Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))
          
class Propertylisting_typeView(APIView):
    def get(self, request, format=None):
        try:
            Propertylistingtypeobj=Propertylisting_type.objects.all().order_by('position')
            serializer=Propertylisting_typeViewSerializer(Propertylistingtypeobj, many=True)
            return Response(util.success(self,serializer.data))
        except Exception as e:
            return Response(util.error(self,str(e)))

class Property_Listing_TypeView(APIView):
    def post(self, request, format=None):
        try:
            data=request.data
            if "Property_listing_type_id" in data:
                if Propertylisting_type.objects.filter(id=data['Property_listing_type_id']):
                    propertyobj=Propertylisting_type.objects.get(id=data['Property_listing_type_id'])
                    propetytypeobj=Property_Listing_Type.objects.filter(type_of_listing=propertyobj)
                    serializer=Property_listing_typeViewSerializer(propetytypeobj, many=True)
                    return Response(util.success(self,serializer.data))
                else:
                    return Response(util.error(self, 'Property_listing_type_id Not valid'))
            else:
                return Response(util.error(self,'Property_listing_type_id not Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class Property_Main_Category_Type_HomeView(APIView):
    def post(self, request, format=None):
        try:
            data=request.data
            if "Property_listing_type_id" in data:
                if Property_Listing_Type.objects.filter(id=data['Property_listing_type_id']):
                    propertylistingtypeobj=Property_Listing_Type.objects.get(id=data['Property_listing_type_id'])
                    # print(propertylistingtypeobj)
                    propertymaincategoryobj=Property_Main_Category.objects.filter(listing_type=propertylistingtypeobj)
                    # print(propertymaincategoryobj)
                    serializer=PropertyMainCategorySerializer(propertymaincategoryobj, many=True)
                    if serializer.data:
                        return Response(util.success(self, serializer.data))  
                    else:
                        return Response(util.error(self, 'no data found'))
                else:
                    return Response(util.error(self, 'Property_listing_type_id Not valid'))
            else:        
                return Response(util.error(self, 'Property_listing_type_id not Found')) 
        except Exception as e:
            return Response(util.error(self,str(e)))       

class Property_Sub_Category_Type_HomeView(APIView):
    def post(self, request, format=None):
        try:
            data=request.data
            if "Property_main_category_id" in data:
                if Property_Main_Category.objects.filter(id=data['Property_main_category_id']):
                    propertymaincategoryobj=Property_Main_Category.objects.get(id=data['Property_main_category_id'])
                    # print(propertymaincategoryobj)
                    if Property_Sub_Category.objects.filter(property_main_category=propertymaincategoryobj):
                        propertysubcategoryobj=Property_Sub_Category.objects.filter(property_main_category=propertymaincategoryobj)
                        # print(propertysubcategoryobj)
                        serializer=PropertySubCategorySerializer(propertysubcategoryobj, many=True)
                        if serializer.data:
                            return Response(util.success(self, serializer.data))  
                        else:
                            return Response(util.error(self, 'no data found'))
                    else:
                        propertysubcategoryobj=Property_Sub_Category.objects.filter(property_main_category=propertymaincategoryobj)
                        # print(propertysubcategoryobj)
                        serializer=PropertySubCategorySerializer(propertysubcategoryobj, many=True)
                        if serializer.data:
                            return Response(util.success(self, serializer.data))  
                        else:
                            return Response(util.error(self, 'no data found'))
                else:
                    return Response(util.error(self, 'Property_listing_type_id Not valid'))
            else:        
                return Response(util.error(self, 'Property_Listing_type_id not Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))  

class Seen_Property_View(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            data=request.data
            # # print(data)
            if  'property_detail_id' in data and 'user_profile_id' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['user_profile_id'])
                if user:
                    if Property_Detail.objects.filter(id=data['property_detail_id']):
                        property_details_obj=Property_Detail.objects.get(id=data['property_detail_id'])
                        if Seen_Property_listing.objects.filter(user_profile_id=user).filter(property_detail_id=property_details_obj):
                            return Response(util.success(self,'Property Already Seen'))
                        else:       
                            obj=Seen_Property_listing.objects.create(property_detail_id=property_details_obj, user_profile_id=user )
                            return Response(util.success(self, "Success"))
                            # # print("obj",obj)
                    else:
                        return Response(util.error(self,"property id is not Valid"))
                else:
                    return Response(util.error(self,'User Id Not valid'))
            else:
                return Response(util.error(self,' property_detail_id,user_profile_id is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class LoadListingTypeAccordingToSetting(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            data=request.data
            if "user_id" in data:
                user,usertype,userprofile=get_user_usertype_userprofile(self,data["user_id"])
                # print(user,usertype,userprofile)
                accountsettingobj=AccountSetting.objects.get(user=user)
                # print(accountsettingobj)
                if accountsettingobj.type_allowed == 0:
                    if Propertylisting_type.objects.filter(property_listing_name="Residential"):
                        propertyobj=Propertylisting_type.objects.get(property_listing_name="Residential")
                        propetytypeobj=Property_Listing_Type.objects.filter(type_of_listing=propertyobj) 
                        serialize=Property_listing_typeViewSerializer(propetytypeobj, many=True)
                        if serialize.data:
                            return Response(util.success(self,serialize.data))
                        else:
                            return Response(util.error(self,"No data found."))
                    else:
                        return Response(util.error(self,"Please add Residential in Propertylisting_type"))
                elif accountsettingobj.type_allowed == 1:
                    if Propertylisting_type.objects.filter(property_listing_name="Commercial"):
                        propertyobj=Propertylisting_type.objects.get(property_listing_name="Commercial")
                        propetytypeobj=Property_Listing_Type.objects.filter(type_of_listing=propertyobj)
                        serialize=Property_listing_typeViewSerializer(propetytypeobj, many=True)
                        if serialize.data:
                            return Response(util.success(self,serialize.data))
                        else:
                            return Response(util.error(self,"No data found."))
                    else:
                        return Response(util.error(self,"Please add Commercial in Propertylisting_type"))
                else:
                    propetytypeobj=Property_Listing_Type.objects.all()
                    serialize=Property_listing_typeViewSerializer(propetytypeobj, many=True)
                    return Response(util.success(self,serialize.data))
            else:
                return Response(util.error(self,"user_id is not found"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class PropertyListingAccordingToPropertyListingType(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            data=request.data
            if "Property_listing_type_id" in data:
                if Property_Listing_Type.objects.filter(id=data['Property_listing_type_id']):
                    propertyobj=Property_Listing_Type.objects.get(id=data['Property_listing_type_id'])
                    propertydetailsobj=Property_Detail.objects.filter(id=propertyobj.id)
                    userprofileagentserializer=PropertyListUserPropfile(propertydetailsobj, many=True)
                    if userprofileagentserializer.data:
                        return Response(util.success(self,{'property':userprofileagentserializer.data}))
                    else:
                        return Response(util.error(self,"No data found."))      
                else:        
                    return Response(util.error(self, ' Property_listing_type ID not Found'))
            else:
                return Response(util.error(self,'Property_listing_type not Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

    def get(self, request, id=None):
        try:
            if Property_Detail.objects.filter(id=id):
                propertydetailobj=Property_Detail.objects.get(id=id)
                userprofileagentserializer=PropertyListUserPropfile(propertydetailobj)
                if userprofileagentserializer.data:
                        return Response(util.success(self,{'property':userprofileagentserializer.data}))
                else:
                    return Response(util.error(self,"No data found.")) 
            else:
                return Response(util.error(self, 'Property_detail_id not Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class SaveAllListing(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            data=request.data
            if 'user_id' in data and 'property_details_id' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['user_id'])
                if user:
                    if Property_Detail.objects.filter(id__in = data['property_details_id']):
                        propertyobj = Property_Detail.objects.filter(id__in = data['property_details_id'])
                        for i in propertyobj:
                            propertyobj1 = Property_Detail.objects.get(id = i.id)
                            if Guest_Users_Save_Listing.objects.filter(user=user, property_details=propertyobj1):
                                pass
                            else:
                                guestobj = Guest_Users_Save_Listing.objects.create(user=user, property_details=propertyobj1,notes = data['notes'], rating = data['rating'])
                        return Response(util.success(self,'Property Save'))
                    else:
                        return Response(util.error(self,'Property Not Found'))
                else:
                    return Response(util.error(self, 'Invalid user'))
            else:
                return Response(util.error(self, 'user_id and property_details_id is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class DeleteAllSaveListing(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            data = request.data
            if 'user_id' in data and 'property_details_id' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['user_id'])
                if user:
                    for i in data['property_details_id']:
                        guestobj = Guest_Users_Save_Listing.objects.filter(user=user, property_details=i)
                        guestobj.delete()
                    return Response(util.success(self, 'Delete Successfully'))
                else:
                    return Response(util.error(self, 'Invalid user'))
            else:
                return Response(util.error(self, 'user_id and property_details_id is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class AminitiesView(APIView):
    def get(self,request,format=None):
        try:
            amenitiesmasterobj=Amenities_Master.objects.all()
            serializer=AmenitiesNasterSerializer(amenitiesmasterobj, many=True)
            if serializer.data:
                return Response(util.success(self,serializer.data))
            else:
                return Response(util.error(self,'Data Not Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class PropertyTypeFilterView(APIView):
    def get(self,request,format=None):
        try:
            PropertyTypefilterobj=Property_Type.objects.all()
            serializer=PropertyTypeFilterSerializer(PropertyTypefilterobj, many=True)
            if serializer.data:
                return Response(util.success(self,serializer.data))
            else:
                return Response(util.error(self,'Data Not Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class InvitationView(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
            if 'userid' in data and 'email' in data and 'first_name' in data and 'last_name' in data and 'license' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['userid'])
                if user:
                    obj=Invitation.objects.filter(userid=user).count()
                    if obj <= 12:
                        expirytime = datetime.datetime.now() + datetime.timedelta(hours=3)
                        invite=Invitation.objects.create(userid=user,email=data['email'],expiration_date=expirytime,first_name=data['first_name'],last_name=data['last_name'],license=data['license'])
                        # current_site = get_current_site(request).domain
                        uid = urlsafe_base64_encode(force_bytes(invite.id))
                        # relativeLink = reverse('accept_invitation')
                        absurl = settings.SITE_URL+'/team-login'
                        send_mail(
                            'Invitation to join our site',
                            'Click the link to accept the invitation:'+absurl+'?uid='+uid+'&'+'token='+str(invite.token),
                            'invitations@example.com',
                            [invite.email],
                            fail_silently=False,
                        )
                        return Response(util.success(self, 'Email Send'))
                    else:
                        return Response(util.error(self, 'Invitation is More than 12'))
                else:
                    return Response(util.error(self, 'user not found'))
            else:
                return Response(util.error(self,'userid and email and first_name and last_name and license must needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class BluckInvitationView(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
            if "user_id" in data and "team_list" in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['user_id'])
                if user:
                    # emails = [team_member['email'] for team_member in data['team_list']]
                    # # print(emails)
                    # if User.objects.filter(email__in=emails).exists():
                    #     return Response(util.error(self, 'The user is already exists'))
                    # else:
                    obj=Invitation.objects.filter(userid=user).count()
                    if obj <= 12:
                        for i in data['team_list']:
                            if Invitation.objects.filter(email=i['email']):
                                pass
                            else:
                                expirytime = datetime.now() + timedelta(hours=3)
                                invite=Invitation.objects.create(userid=user,email=i['email'],expiration_date=expirytime,first_name=i['first_name'],last_name=i['last_name'],license=i['license'])
                                uid = urlsafe_base64_encode(force_bytes(invite.id))
                                absurl = settings.SITE_URL+'team-login'
                                send_mail(
                                    'Invitation to join our site',
                                    'Click the link to accept the invitation:'+absurl+'?uid='+uid+'&'+'token='+str(invite.token),
                                    'invitations@example.com',
                                    [invite.email],
                                    fail_silently=False,
                                )
                        return Response(util.success(self, 'Invitation E-mail send Successfully!'))
                    else:
                        return Response(util.error(self, 'Invitation is More than 12'))
                else:
                    return Response(util.error(self, 'User is not valid'))
            else:
                return Response(util.error(self,'user_id and team_list must needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class UpdateTeamMember(APIView):
    def put(self, request, format=None, id=None):
        try:
            if id is not None:
                if Invitation.objects.filter(id=id):
                    expirytime = datetime.now() + timedelta(hours=3)
                    obj=Invitation.objects.get(id=id)
                    # print(obj.email)
                    if obj.email==request.data['email']:
                        obj.is_accept = request.data['is_accept']
                    else:
                        obj.email=request.data['email']
                        obj.is_accept = False
                    # obj.email=request.data['email']
                    obj.expiration_date=expirytime
                    obj.first_name=request.data['first_name']
                    obj.last_name=request.data['last_name']
                    obj.license=request.data['license']
                    obj.save()
                    # current_site = get_current_site(request).domain
                    uid = urlsafe_base64_encode(force_bytes(obj.id))
                    # relativeLink = reverse('accept_invitation')
                    absurl = settings.SITE_URL+'/team-login'
                    send_mail(
                        'Invitation to join our site',
                        'Click the link to accept the invitation:'+absurl+'?uid='+uid+'&'+'token='+str(obj.token),
                        'invitations@example.com',
                        [obj.email],
                        fail_silently=False,
                    )
                    return Response(util.success(self, 'Updated Successfully And Email Send'))
                else:
                    return Response(util.error(self, "Data not Valid"))
            else:
                return Response(self, "id is required")
        except Exception as e:
            return Response(util.error(self,str(e)))

class RegistrationAgentAPI(APIView):
    def post(self, request, format = None):
        try:
            data=request.data
            agent_profile=False
            agentsubscription=False
            add_on=False
            nb_sb=False
            billing = False
            license_approve = False
            if "uid" in data and "password" in data:
                uid = request.data.get("uid")
                id = smart_str(urlsafe_base64_decode(uid))
                teammember = Invitation.objects.get(id = id)
                if teammember.expiration_date < timezone.now():
                    return Response(util.error(self,'Invitation has expired'))
                else:
                    if User.objects.filter(username=teammember.email):
                        user_object=User.objects.get(username=teammember.email)
                        if user_object.is_superuser is False:
                            user=authenticate(username=user_object.username,password=data['password'])
                            if user is not None:
                                token = get_tokens_for_user(user)
                                login(request, user)
                                usertypeobj=UserType.objects.get(user=user)
                    else:
                        user=User.objects.create_user(username=teammember.email,email=teammember.email,first_name=teammember.first_name,last_name=teammember.last_name,password=data['password'], is_active=True)
                        usertypeobj=UserType.objects.create(user=user,user_type=2)
                        userprofile = UserProfile.objects.create(user_type=usertypeobj,first_name=teammember.first_name,last_name=teammember.last_name,unique_id="Sub")
                    
                    User_Log.objects.create(user_type=usertypeobj,action_type=data['user_log']['action_type'],date_time=data['user_log']['date_time'],ip_address=data['user_log']['ip_address'],longitude=data['user_log']['longitude'],latitude=data['user_log']['latitude'],
                    mac_address=data['user_log']['mac_address'],location=data['user_log']['location'])
                    teammember.is_accept = True
                    teammember.save()
                    user, usertype, userprofile=get_user_usertype_userprofile(request, user.id)
                    token = get_tokens_for_user(user)
                    if userprofile and AgentLic.objects.filter(user=user).exists():
                        agent_profile=True
                    if AgentLic.objects.filter(user=user, is_validated=True).exists():
                        license_approve = True
                    if AgentApprovedSubscriptionPlan.objects.filter(user=user).exists():
                        agentsubscription=True
                        if AgentApprovedSubscriptionPlan.objects.filter(user=user).count()>1:
                            add_on=True
                    if add_on == True and Nb_specality_area.objects.filter(user=user).exists():
                        nb_sb=True
                    if Billing.objects.filter(user=user).exists():
                        billing = True
                    profileserializer = UserProfileSerializer(userprofile)
                    serializer = ProfileImageSerializer(userprofile)
                    return Response(util.success(self,{'user_info':{'id':user.id,'username':user.username,'usertypeobj':usertypeobj.user_type,"agent_profile":agent_profile, "agentsubscription":agentsubscription, "add_on":add_on, "nb_sb":nb_sb, "billing":billing, "license_approve":license_approve, "is_social":user.is_social},'token':token,'msg':'login Success','profile':profileserializer.data,'image': serializer.data}))
            else:
                return Response(util.error(self,"uid and password are required"))
        except Exception as e:
            return Response(util.error(self,str(e)))
        
class RemoveTeamMember(APIView):
    def delete(self, request, format=None, id=None):
        try:
            if id is not None:
                if Invitation.objects.filter(id = id).exists():
                    TeamMember = Invitation.objects.get(id = id)
                    TeamMember.delete()
                    return Response(util.success(self, "Deleted Successfully"))
                else:
                    return Response(util.error(self, "Data Not Found"))
            return Response(util.error(self, "id is required"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class filter_save_serach_get(APIView):
    def get(self, request, format=None, id=None):
        try:
            if id is not None:
                user,usertype, userprofile=get_user_usertype_userprofile(request, id)
                if user:
                    if filter_save_serach.objects.filter(user=user):
                        filtersaveserachobj=filter_save_serach.objects.filter(user=user)
                        serializer=FilterSaveSerachNameSerializer(filtersaveserachobj, many=True)
                        if serializer.data:
                            return Response(util.success(self,serializer.data))
                        else:
                            return Response(util.error(self,'Data Not Found'))
                    else:
                        return Response(util.error(self,'filter_save_serach not found')) 
                else:
                    return Response(util.error(self,'user_id is needed')) 
        except Exception as e:
            return Response(util.error(self,str(e)))

class Filter(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None, id=None):
        try:
            user_id=request.GET.get('user_id',None)
            if id is not None:
                filterobj = filter_save_serach.objects.get(id = id)
                main_categoryobj =Property_Main_Category.objects.get(id = filterobj.propertymaincategory.id) # get main category
                propertylistingobj = Propertylisting_type.objects.get(id = filterobj.Type.type_of_listing.id) # get Residential and Commercial
                typeobj = Property_Listing_Type.objects.get(id=filterobj.Type.id) # get rental and leasing

                if propertylistingobj.property_listing_name == "Residential":
                    propertyobj = Property_Detail.objects.filter(property_listing_type = propertylistingobj.id, propertylisting_type = typeobj.id, property_main_category = main_categoryobj.id)

                    if filterobj.Bedrooms != None:
                        propertyobj = propertyobj.filter(Bedrooms__gte = filterobj.Bedrooms)
                    
                    if filterobj.Bathrooms != None:
                        propertyobj = propertyobj.filter(Bathrooms__gte = filterobj.Bathrooms)
                    
                    # if filterobj.Amenities_filter != None:
                    #     property_detail_obj_id=propertyobj.values_list('id',flat=True)
                    #     propertyobj=Property_Amenities.objects.filter(property_details__in=property_detail_obj_id)

                else:
                    propertyobj = Property_Detail.objects.filter(property_listing_type = propertylistingobj.id, propertylisting_type = typeobj.id, property_main_category = main_categoryobj.id)

                    if filterobj.propertysubcategory != None:
                        sub_categoryobj = Property_Sub_Category.objects.get(id = filterobj.propertysubcategory.id)
                        propertyobj = propertyobj.filter(property_sub_category = sub_categoryobj.id)
                    
                    if filterobj.units != None:
                        propertyobj = propertyobj.filter(Units__gte = filterobj.units)
                    
                    if filterobj.room != None:
                        propertyobj = propertyobj.filter(Rooms__gte = filterobj.room)
                    
                    if filterobj.block != None:
                        propertyobj = propertyobj.filter(Block__gte = filterobj.block)
                    
                    if filterobj.lot != None:
                        propertyobj = propertyobj.filter(Lot__gte = filterobj.lot)
                    
                    if filterobj.lot_diamensions != None:
                        propertyobj = propertyobj.filter(Lot_Dimensions__gte = filterobj.lot_diamensions)
                    
                    if filterobj.building_diamensions != None:
                        propertyobj = propertyobj.filter(Building_Dimension__gte = filterobj.building_diamensions)
                    
                    if filterobj.stories != None:
                        propertyobj = propertyobj.filter(Stories__gte = filterobj.stories)
                    
                    if filterobj.Zone != None:
                        propertyobj = propertyobj.filter(Zone__gte = filterobj.Zone)

                    if filterobj.far != None:
                        propertyobj = propertyobj.filter(FAR__gte = filterobj.far)
                    
                    if filterobj.Assessment != None:
                        propertyobj = propertyobj.filter(Assessment__gte = filterobj.Assessment)
                    
                    if filterobj.Annual_Taxes != None:
                        propertyobj = propertyobj.filter(Annual_Taxes__gte = filterobj.Annual_Taxes)
                    
                    if filterobj.Available_Air_Rights != None:
                        propertyobj = propertyobj.filter(Available_Air_Rights__gte = filterobj.Available_Air_Rights)
                
                areaobj = None
                cityobj = None
                stateobj = None
                countryobj = None

                if filterobj.area != None:
                    if AreaMaster.objects.filter(id=filterobj.area.id):
                        areaobj = AreaMaster.objects.get(id=filterobj.area.id)
                
                if filterobj.city != None:
                    if CityMaster.objects.filter(id=filterobj.city.id):
                        cityobj = CityMaster.objects.get(id=filterobj.city.id)
                
                if filterobj.state != None:
                    if StateMaster.objects.filter(id=filterobj.state.id):
                        stateobj = StateMaster.objects.get(id=filterobj.state.id)
                        
                if filterobj.country != None:
                    if CountryMaster.objects.filter(id=filterobj.country.id):
                        countryobj = CountryMaster.objects.get(id=filterobj.country.id)

                if areaobj != None:
                    propertyobj = propertyobj.filter(property_area = areaobj.id)
                
                if cityobj != None:
                    propertyobj = propertyobj.filter(property_city = cityobj.id)
                
                if stateobj != None:
                    propertyobj = propertyobj.filter(property_state = stateobj.id)
                
                if countryobj != None:
                    state_obj = StateMaster.objects.filter(country_master = countryobj.id)
                    propertyobj = propertyobj.filter(property_state__in = state_obj)

                if filterobj.Squft_max != None or filterobj.Squft_min != None:
                    propertyobj = propertyobj.filter(Square_sqft__gte=str(filterobj.Squft_min)).filter(Square_sqft__lte=str(filterobj.Squft_max))
                    

                if filterobj.Price_Max != None or filterobj.Price_Min != None:
                    propertyobj = propertyobj.filter(property_listing_amount__gte=str(filterobj.Price_Min)).filter(property_listing_amount__lte=str(filterobj.Price_Max))

                paginator = MyPagination()
                paginated_queryset = paginator.paginate_queryset(propertyobj, request)
                serializer = PropertySerializer(paginated_queryset, context={'user_id': user_id}, many=True)
                if serializer.data:
                    return Response(util.success(self, {"porperty":serializer.data}))
                else:
                    return Response(util.error(self, "Data Not Found"))
                
            else:
                return Response(util.error(self, "id is required"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class Filter_Save_Search(APIView):
    def post(self, request, format=None):
        try:
            data=request.data
            if "category" in data and "type" in data and "user_id" in data and "filter_name" in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['user_id'])
                if Property_Main_Category.objects.filter(id=data["type"]):
                    categoryobj = Property_Listing_Type.objects.get(id=data['category'])
                    tyepobj=Property_Main_Category.objects.get(id=data['type'])
                    if tyepobj.Main_category == "Leisure":
                        if 'Sub_category' in data:
                            if Property_Sub_Category.objects.filter(id=data['Sub_category']):
                                propertysubcategoryobj=Property_Sub_Category.objects.get(id=data['Sub_category'])
                                filtersaveobj=filter_save_serach.objects.create(Type = categoryobj,filterName=data['filter_name'],propertymaincategory=tyepobj,user=user,propertysubcategory=propertysubcategoryobj)
                            else:
                                return Response(util.error(self, 'Sub_category details not found'))
                        else:
                            return Response(util.error(self,'Sub_category is needed'))
                    else:
                        tyepobj=Property_Main_Category.objects.get(id=data['type'])
                        filtersaveobj=filter_save_serach.objects.create(Type = categoryobj,filterName=data['filter_name'],propertymaincategory=tyepobj,user=user)
                    
                    if data["Bedrooms"] is not None:
                        filtersaveobj.Bedrooms=data["Bedrooms"]
                    if data["Bathrooms"] is not None:
                        filtersaveobj.Bathrooms=data["Bathrooms"]  
                    if data["units"] is not None:
                        filtersaveobj.units=data["units"]
                    if data["room"] is not None:
                        filtersaveobj.room=data["room"]
                    if data['cost_type'] is not None:
                        if data['cost_type'] == "1":
                            filtersaveobj.monthly = True
                        else:
                            filtersaveobj.cost_per_square_fit = True
                    # if  'monthly' in data:
                    #     filtersaveobj.monthly=data["monthly"]    
                    # if  'cost_per_square_fit' in data:
                    #     filtersaveobj.cost_per_square_fit=data["cost_per_square_fit"]
                    if data["block"] is not None:
                        filtersaveobj.block=data["block"]
                    if data["lot"] is not None:
                        filtersaveobj.lot=data["lot"]
                    if data["Zone"] is not None:
                        filtersaveobj.Zone=data["Zone"]
                    if data["lot_diamensions"] is not None:
                        filtersaveobj.lot_diamensions=data["lot_diamensions"]
                    if data["building_diamensions"] is not None:
                        filtersaveobj.building_diamensions=data["building_diamensions"]
                    if data["stories"] is not None:
                        filtersaveobj.stories=data["stories"]
                    if data["far"] is not None:
                        filtersaveobj.far=data["far"]
                    if data["Assessment"] is not None:
                        filtersaveobj.Assessment=data["Assessment"]
                    if data["Annual_Taxes"] is not None:
                        filtersaveobj.Annual_Taxes=data["Annual_Taxes"]
                    if data["Available_Air_Rights"] is not None:
                        filtersaveobj.Available_Air_Rights=data["Available_Air_Rights"]
                    if data["Squft_min"] is not None:
                        filtersaveobj.Squft_min=data["Squft_min"]
                    if data["Squft_max"] is not None:
                        filtersaveobj.Squft_max=data["Squft_max"]
                    if data["pricemin"] is not None:
                        filtersaveobj.Price_Min=data["pricemin"]
                    if data["pricemax"] is not None:
                        filtersaveobj.Price_Max=data["pricemax"]
                    if data["Amenities_filter"] is not None:
                        filtersaveobj.Amenities_filter=data["Amenities_filter"]
                    if data["area"] is not None:
                        areaobj=AreaMaster.objects.get(id=data["area"])    
                        filtersaveobj.area=areaobj
                    if data["city"] is not None:
                        cityobj=CityMaster.objects.get(id=data["city"])
                        filtersaveobj.city=cityobj  
                    if data["state"] is not None:
                        stateobj=StateMaster.objects.get(id=data["state"])
                        filtersaveobj.state=stateobj
                    if data["country"] is not None:
                        countryobj=CountryMaster.objects.get(id=data["country"])
                        filtersaveobj.country=countryobj
                    filtersaveobj.save()
                    return Response(util.success(self, 'Filter save'))
                else:
                    return Response(util.error(self,'property_main_category details not found'))
            else:
                return Response(util.error(self, 'Property_main_category_id, user_id, Type,filter_name needed' ))
        except Exception as e:
            return Response(util.error(self,str(e)))
    
    def delete(self, request, format = None, id=None):
        try:
            if id is not None:
                filtersaveobj=filter_save_serach.objects.get(id= id)
                filtersaveobj.delete()
                return Response(util.success(self, 'Delete Successfully'))
            else:
                return Response(util.error(self,"id is required"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class TeamMemberProfile(APIView):
    def get(self, request, format=None, slug=None):
        try:
            if slug is not None:
                userprofileobjid = UserProfile.objects.get(slug = slug)
                user,usertype, userprofile=get_user_usertype_userprofile(request, userprofileobjid.user_type.user.id)
                if userprofile:
                    inviteopbj=Invitation.objects.filter(userid=user, is_accept=True)
                    emailobj=[]
                    for i in inviteopbj:
                        emailobj.append(i.email)
                    userobj=User.objects.filter(email__in=emailobj)
                    usertypeobj=UserType.objects.filter(user__in=userobj)
                    userprofileobj=UserProfile.objects.filter(user_type__in=usertypeobj)
                    serializer = UserProfileSerializer(userprofileobj, many=True)
                    if serializer.data:
                        return Response(util.success(self, serializer.data))
                    else:
                        return Response(util.error(self, 'No data Found'))
                else:
                    return Response(util.error(self, 'No data Found'))
            else:
                return Response(util.error(self, 'user_id is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))


def porpertylisting_type(propertyobj,userobj):
    agentobj = AgentApprovedSubscriptionPlan.objects.filter(user__in=list(set(userobj)))
    propertylistobj = Propertylisting_type.objects.get(id=propertyobj)
    userid=[]
    for i in agentobj:
        if propertylistobj.property_listing_name == "Residential":
            if i.plan_id.Name == "Residential":
                userid.append(i.user.id)
            else:
                pass
        else:
            if i.plan_id.Name == "Commercial":
                userid.append(i.user.id)
            else:
                pass
    return userid

class Property_Neighbourhood(APIView):
    def post(self, request, format=None):
        try:
            propertyobj = request.POST.get('property_id')
            areaid=request.POST.get('area_id')
            cityid=request.POST.get('city_id')
            stateid=request.POST.get('state_id')
            countryid=request.POST.get('country_id')
            userobj1=[]
            # area
            if areaid is not None:
                neighbourhood_spicialityobj=Nb_specality_area.objects.filter(area_id__icontains = areaid)
                for i in neighbourhood_spicialityobj:
                    userobj1.append(i.user.id)
                obj = porpertylisting_type(propertyobj,userobj1)
                userobj = User.objects.filter(id__in=obj)
                usertypeobj = UserType.objects.filter(user__in=userobj)
                userprofileobj = UserProfile.objects.filter(user_type__in=usertypeobj)
                serializer = UserProfileSerializer(userprofileobj, many=True)
                if serializer.data:
                    return Response(util.success(self, serializer.data))
                else:
                    return Response(util.error(self, 'No Data Found'))

            # city
            elif areaid is None and cityid is not None:
                cityobj = CityMaster.objects.filter(id=cityid)
                areaobj = AreaMaster.objects.filter(city_master__in=cityobj)
                for i in areaobj:
                    neighbourhood_spicialityobj=Nb_specality_area.objects.filter(area_id__icontains = i.id)
                    # print(neighbourhood_spicialityobj)
                    for i in neighbourhood_spicialityobj:
                        userobj1.append(i.user.id)
                obj = porpertylisting_type(propertyobj,userobj1)
                userobj = User.objects.filter(id__in=obj)
                usertypeobj = UserType.objects.filter(user__in=userobj)
                userprofileobj = UserProfile.objects.filter(user_type__in=usertypeobj)
                serializer = UserProfileSerializer(userprofileobj, many=True)
                if serializer.data:
                    return Response(util.success(self, serializer.data))
                else:
                    return Response(util.error(self, 'No Data Found'))
            # State
            elif areaid is None and cityid is None and stateid is not None:
                stateobj=StateMaster.objects.filter(id=stateid)
                cityobj = CityMaster.objects.filter(state_master__in=stateobj)
                areaobj = AreaMaster.objects.filter(city_master__in=cityobj)
                for i in areaobj:
                    neighbourhood_spicialityobj=Nb_specality_area.objects.filter(area_id__icontains = i.id)
                    # print(neighbourhood_spicialityobj)
                    for i in neighbourhood_spicialityobj:
                        userobj1.append(i.user.id)
                obj = porpertylisting_type(propertyobj,userobj1)
                userobj = User.objects.filter(id__in=obj)
                usertypeobj = UserType.objects.filter(user__in=userobj)
                userprofileobj = UserProfile.objects.filter(user_type__in=usertypeobj)
                serializer = UserProfileSerializer(userprofileobj, many=True)
                if serializer.data:
                    return Response(util.success(self, serializer.data))
                else:
                    return Response(util.error(self, 'No Data Found'))
            # Country
            elif areaid is None and cityid is None and stateid is None and countryid is not None:
                countryobj=CountryMaster.objects.filter(id=countryid)
                stateobj=StateMaster.objects.filter(country_master__in=countryobj)
                cityobj = CityMaster.objects.filter(state_master__in=stateobj)
                areaobj = AreaMaster.objects.filter(city_master__in=cityobj)
                for i in areaobj:
                    neighbourhood_spicialityobj=Nb_specality_area.objects.filter(area_id__icontains = i.id)
                    # print(neighbourhood_spicialityobj)
                    for i in neighbourhood_spicialityobj:
                        userobj1.append(i.user.id)
                obj = porpertylisting_type(propertyobj,userobj1)
                userobj = User.objects.filter(id__in=obj)
                usertypeobj = UserType.objects.filter(user__in=userobj)
                userprofileobj = UserProfile.objects.filter(user_type__in=usertypeobj)
                serializer = UserProfileSerializer(userprofileobj, many=True)
                if serializer.data:
                    return Response(util.success(self, serializer.data))
                else:
                    return Response(util.error(self, 'No Data Found'))
            else:    
                return Response(util.error(self, 'area_id or city_id or state_id or country_id is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class TeamMemberShow(APIView):
    def get(self, request, format=None, slug= None):
        try:
            if id is not None:
                if Property_Detail.objects.filter(slug=slug):
                    propertyobj=Property_Detail.objects.get(slug=slug)
                    teamobj = TeamProperty.objects.filter(propertydetail_id = propertyobj.id)
                    userprofileid=[]
                    for i in teamobj:
                        userprofileid.append(i.userprofile_id.id)
                    userprofileobj = UserProfile.objects.filter(id__in=userprofileid)
                    serializer = UserProfileTemaleaderSerializer(userprofileobj, many=True)
                    if serializer.data:
                        return Response(util.success(self, serializer.data))
                    else:
                        return Response(util.error(self, 'No data Found'))
                else:
                    return Response(util.error(self, 'Property Deatils not found'))
            else:
                return Response(util.error(self, "id is required"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class Contact_Now(APIView):
    def post(self, request, format = None):
        try:
            data = request.data
            if 'agent_id' in data and 'user_id' in data and 'message' in data:
                if User.objects.filter(id=data['user_id']):
                    user,usertype,userprofile=get_user_usertype_userprofile(request, data['user_id'])
                    agentarr=User.objects.filter(id__in=data['agent_id'])
                    for i in agentarr:
                        send_mail(
                            'You receive a message from' + user.email,
                            data['message'],
                            'contact@example.com',
                            [i.email],
                            fail_silently=False,
                        )
                        # agentobj=UserProfile.objects.get(id=i.id)
                        # for j in data['property_id']:
                        #     propertyobj = Property_Detail.objects.get(id=j)
                        #     contactnowobj=ContactNow.objects.create(userid = userobj, userprofile_id=agentobj, message=data['message'], property_id = propertyobj)
                    return Response(util.success(self, 'Successfully Send a Message'))
                else:
                    return Response(util.error(self, 'user_id not found'))
            else:
                return Response(util.error(self, 'Agent_id, user_id, message is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class GetPropertyBasedOnLocation(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        cityid=request.GET.get('cityid',None)
        user_id=request.GET.get('userid','')
        accountsettingsobj=None
        if AccountSetting.objects.filter(user=user_id):
            accountsettingsobj=AccountSetting.objects.get(user=user_id)
        
        if accountsettingsobj is not None:
            if accountsettingsobj.type_allowed==0:
                propertylostingobj=Propertylisting_type.objects.get(property_listing_name="Residential")
            else:
                propertylostingobj=Propertylisting_type.objects.get(property_listing_name="Commercial")


            if cityid is not None:
                property_detail_obj=Property_Detail.objects.filter(property_city=cityid).filter(property_listing_type=propertylostingobj)
                paginator = MyPagination()
                paginated_queryset = paginator.paginate_queryset(property_detail_obj, request)
                # serializer = PropertySerializer(paginated_queryset, many=True)
                serializer = PropertySerializer(paginated_queryset, context={'user_id': user_id}, many=True)
                if serializer.data:
                    return Response(util.success(self, {"porperty":serializer.data}))
                else:
                    return Response(util.error(self, "Data Not Found"))
            else:
                return Response(util.error(self, 'id is required'))
        else:
            return Response(util.error(self, "Data Not Found"))

class GetPropertyDetail(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            property_id=request.GET.get('propertyid',None)
            user_id=request.GET.get('userid',None)
            propertydetail=Property_Detail.objects.get(slug=property_id)
            serializer=PropertySerializer(propertydetail,context={'user_id': user_id})
            return Response(util.success(self, {"porperty":serializer.data}))
        except:
            return Response(util.error(self, "Invalid Data"))

class GetPropertyAmenities(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            property_id=request.GET.get('propertyid',None)
            propertydetail=Property_Detail.objects.get(slug=property_id)
            propety_amenities_obj = Property_Amenities.objects.filter(property_details=propertydetail)
            serializer=PropertyamenitiesSeriallizer(propety_amenities_obj, many=True)
            if serializer.data:
                return Response(util.success(self, {"amenities":serializer.data}))
            else:
                return Response(util.error(self, "Data Not Found"))
        except:
            return Response(util.error(self, "Invalid Data"))

class GetPropertyImage(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            property_id=request.GET.get('propertyid',None)
            propertydetail=Property_Detail.objects.get(slug=property_id)
            property_image_obj = Property_Image.objects.filter(property_detail_id=propertydetail)
            serializer=PropertyImageSerializer(property_image_obj, many=True)
            if serializer.data:
                return Response(util.success(self, {"image":serializer.data}))
            else:
                return Response(util.error(self, "Data Not Found"))
        except:
            return Response(util.error(self, "Invalid Data"))

class GetPropertySpaces(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            property_id=request.GET.get('propertyid',None)
            propertydetail=Property_Detail.objects.get(slug=property_id)
            property_spaces_obj = Property_Space_Availability.objects.filter(Property=propertydetail)
            serializer=PropertySpaceAvaliableSerializer(property_spaces_obj, many=True)
            if serializer.data:
                return Response(util.success(self, {"spaces":serializer.data}))
            else:
                return Response(util.error(self, "Data Not Found"))
        except:
            return Response(util.error(self, "Invalid Data"))

class GetNeibourhoodBasedOnLocation(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            cityid=request.GET.get('cityid',None)
            cityobj = CityMaster.objects.get(id = cityid)
            areaobj = AreaMaster.objects.filter(city_master = cityobj.id)
            userobj1=[]
            for areaobj in areaobj:
                neighbourhood_spicialityobj=Nb_specality_area.objects.filter(area_id__icontains = areaobj.id, is_verified = "Approve")
                for i in neighbourhood_spicialityobj:
                    userobj1.append(i.user.id)
            userobj = User.objects.filter(id__in=userobj1)
            usertypeobj = UserType.objects.filter(user__in=userobj)
            userprofileobj = UserProfile.objects.filter(user_type__in=usertypeobj)
            serializer = NeighborAvaliableProfileSerializer(userprofileobj, many=True)
            if serializer.data:
                return Response(util.success(self, {"neighbourhood":serializer.data}))
            else:
                return Response(util.error(self, "Data Not Found"))
        except:
            return Response(util.error(self, "Invalid Data"))

class GetlistingDate(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            property_id=request.GET.get('propertyid',None)
            propertydetail=Property_Detail.objects.get(slug=property_id)
            available_from = propertydetail.created_date
            new_date_string = available_from.strftime('%d/%m/%Y')
            total_day = datetime.date.today()-available_from

            Type = propertydetail.property_main_category.Main_category
            return Response(util.success(self, {"Available":new_date_string, "Time_on_MLS-tutor":total_day.days,"Type":Type}))
        except:
            return Response(util.error(self, "Invalid Data"))

class Get30min(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            property_id=request.GET.get('propertyid',None)
            propertydetail=Property_Detail.objects.get(slug=property_id)
            property_30min_obj = Property30minshow.objects.filter(property_details=propertydetail).last()
            serializer=Get30minSerilizer(property_30min_obj)
            if serializer.data:
                return Response(util.success(self, serializer.data))
            else:
                return Response(util.error(self, "Data Not Found"))
        except:
            return Response(util.error(self, "Invalid Data"))

class Rating_Review(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format= None, id = None):
        try:
            if id is not None:
                user,usertype, userprofile=get_user_usertype_userprofile(request, id)
                if user:
                    reviewobj = Review.objects.filter(user=user)
                    serializer = ReviewSerializer(reviewobj, many=True)
                    if serializer.data:
                        return Response(util.success(self, serializer.data))
                    else:
                        return Response(util.success(self, "No Data Found"))
                else:
                    return Response(util.error(self, "user is not valid"))
            else:
                return Response(util.success(self, "success"))
        except Exception as e:
            return Response(util.error(self,str(e)))
    
    def post(self, request, format = None, id = None):
        try:
            if id is not None:
                data = request.data
                user,usertype, userprofile=get_user_usertype_userprofile(request, id)
                if user:
                    if "AgentUser" in data:
                        if UserProfile.objects.filter(id = data["AgentUser"]):
                            userprofileobj = UserProfile.objects.get(id = data["AgentUser"])
                            if Review.objects.filter(AgentUser = userprofileobj, user = user):
                                return Response(util.error(self, "Already Reacted"))
                            else:
                                reviewobj = Review.objects.create(
                                    AgentUser = userprofileobj, user = user, meet = data["meet"], Knowledge = data["Knowledge"], Professionalism = data["Professionalism"],Customer_Service = data["Customer_Service"], Respectful = data["respectful"], Recommend = data["Recommend"], experience = data["experience"], created_date = data["created_date"]
                                )
                                Rating = Review.objects.filter(AgentUser = userprofileobj).aggregate(Avg('Recommend'))
                                userprofileobj.rating = round(Rating['Recommend__avg'], 1)
                                userprofileobj.save()
                                return Response(util.success(self, "Thank You for giving Rating"))
                        else:
                            return Response(util.error(self, "AgentUser is not valid"))
                    else:
                        return Response(util.error(self, "AgentUser are required"))
                else:
                    return Response(util.error(self, "user is not valid"))
            else:
                return Response(util.error(self, "id is not valid"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class ShowAgentMemeber(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, format=None, id = None):
        try:
            if id is not None:
                user,usertype, userprofile=get_user_usertype_userprofile(request, id)
                if user:
                    teammemebershow = Invitation.objects.filter(userid = user, is_accept = True)
                    emailobj=[]
                    for i in teammemebershow:
                        emailobj.append(i.email)
                    userobj=User.objects.filter(email__in=emailobj)
                    usertypeobj=UserType.objects.filter(user__in=userobj)

                    userprofileobj=UserProfile.objects.filter(user_type__in=usertypeobj).values_list("id", flat=True)
                    userprofileid = []
                    for userid in userprofileobj:
                        userprofileid.append(userid)

                    reviewobj = Review.objects.filter(user = user).values_list("AgentUser",flat=True)
                    review = []
                    for reviewobj in reviewobj:
                            review.append(reviewobj)

                    userprofileid=[userobj for userobj in userprofileid if userobj not in review]
                    # for userobj in userprofileid:
                    #     if userobj in review:
                    #         userprofileid.remove(userobj)
                    #     else:
                    #         pass
                    
                    userprofileidobj=UserProfile.objects.filter(id__in=userprofileid)
                    serializer = UserProfileSerializer(userprofileidobj, many=True)
                    if serializer.data:
                        return Response(util.success(self, serializer.data))
                    else:
                        return Response(util.error(self, 'No data Found'))
                    
                else:
                    return Response(util.error(self, "User is not valid"))
            else:
                return Response(util.error(self, "id is not valid"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class RemoveNoLongerAvaliable(APIView):
    def delete(self, request, format=None, id = None):
        try:
            if id is not None:
                user,usertype, userprofile=get_user_usertype_userprofile(request, id)
                if user:
                    propertyobj = Property_Detail.objects.filter(is_property_open = False)
                    guestobj = Guest_Users_Save_Listing.objects.filter(user=user,property_details__in=propertyobj)
                    # # print(guestobj)
                    remove=[]
                    for i in guestobj:
                        if i.property_details.is_property_open == False:
                            remove.append(i.property_details)
                        i.delete()
                    if len(remove)>0:
                        return Response(util.success(self, "Delete Successfully"))
                    else:
                        return Response(util.error(self, "No more open property"))
                else:
                    return Response(util.error(self, "User is not valid"))
            else:
                return Response(util.error(self, "id is not valid"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class UpdateSaveListing(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, format=None):
        try:
            guestobj = Guest_Users_Save_Listing.objects.filter(id=request.data['id']).last()
            guestobj.notes = request.data.get('notes')
            guestobj.rating = request.data.get('rating')
            guestobj.save()
            return Response(util.success(self, 'Successfully updated'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class GetTermsOffer(APIView):
    def get(self, request, format = None):
        try:
            termsobj = Terms.objects.all()
            termserializer = GetTermsSerilizer(termsobj, many=True)
            offerobj = Offer.objects.all()
            offerserializer = GetOfferSerilizer(offerobj, many=True)
            if termserializer.data:
                if offerserializer.data:
                    return Response(util.success(self, {"Terms":termserializer.data, "Offer":offerserializer.data}))
                else:
                    return Response(util.success(self, {"Terms":termserializer.data, "Offer":offerserializer.data}))
            else:
                return Response(util.error(self, "Data Not Found"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class ReafreshAPI(APIView):
    def post(self, request, format = None):
        try:
            data = request.data
            if data['user'] is not None and data['property_id'] is not None and data['current_date'] is not None:
                user,usertype, userprofile=get_user_usertype_userprofile(request, data['user'])
                if user:
                    propertyevnetobj = Property_listing_event.objects.filter(property_details__in = data['property_id'])
                    for i in propertyevnetobj:
                        # if i.property_listing_end_date is None:
                        today = datetime.strptime(data['current_date'], "%Y-%m-%d")
                        i.property_listing_start_date = today
                        # else:
                        #     minusday = i.property_listing_end_date - i.property_listing_start_date
                        #     today = datetime.datetime.strptime(data['current_date'], "%Y-%m-%d")
                        #     futuredate = today + datetime.timedelta(days=minusday.days)

                        #     i.property_listing_start_date = today
                        #     i.property_listing_end_date = futuredate
                        i.save()
                    return Response(util.success(self, 'Successfully Refresh'))
                else:
                    return Response(util.error(self,'user not found'))
            else:
                return Response(util.error(self,'user, property_id and current_date is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class ListingSlugid(APIView):
    def get(self, request, format=None, id=None):
        try:
            user,usertype, userprofile=get_user_usertype_userprofile(request, id)
            if userprofile:
                propertyobj = Property_Detail.objects.filter(user_profile = userprofile, is_property_open = True)
                serializer = ListingSlugSerializers(propertyobj, many=True)
                if serializer.data:
                    return Response(util.success(self,serializer.data))
                else:
                    return Response(util.error(self,"No data Found"))
            else:
                return Response(util.error(self, 'Invalid User Profile'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class RemoveTeam(APIView):
    def delete(self, request, id=None):
        try:
            if id is not None:
                user,usertype, userprofile=get_user_usertype_userprofile(request, id)
                if userprofile:
                    profileobj = UserProfile.objects.get(id = userprofile.id)
                    profileobj.create_team = False
                    profileobj.team_name = None
                    profileobj.save()
                    invitationobj = Invitation.objects.filter(userid = user).filter(is_accept=True).values_list('email', flat=True)
                    userobj = User.objects.filter(email__in = invitationobj).values_list("id", flat=True)
                    usertypeobj = UserType.objects.filter(user__in = userobj).values_list("id", flat=True)
                    userprofileobj = UserProfile.objects.filter(user_type__in = usertypeobj).values_list("id", flat=True)
                    teampropertyobj = TeamProperty.objects.filter(userprofile_id__in = userprofileobj).delete()
                    propertyobj = Property_Detail.objects.filter(user_profile__in = userprofileobj)
                    for i in propertyobj:
                        i.user_profile = profileobj
                        i.save()
                    invitationid = Invitation.objects.filter(userid = user).delete()

                    return Response(util.success(self, 'Delete Successfully'))
                else:
                    return Response(util.error(self, 'Inavlid user'))
            else:
                return Response(util.error(self, 'id is invalid'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class StateDashboard(APIView):
    def get(self, request, format=None):
        try:
            stateobj = StateMaster.objects.all()
            serializer = StateSerializer(stateobj, many=True)
            if serializer.data:
                return Response(util.success(self,serializer.data))
            else:
                return Response(util.error(self, 'No Data Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))
        
class CityDependentState(APIView):
    def get(self, request, format=None):
        try:
            state = request.GET.get('state','')
            if StateMaster.objects.filter(id = state):
                stateobj = StateMaster.objects.get(id = state)
                cityobj = CityMaster.objects.filter(state_master = stateobj)
                serializer = CitySerializer(cityobj, many=True)
                if serializer.data:
                    return Response(util.success(self,serializer.data))
                else:
                    return Response(util.error(self, 'No Data Found'))
            else:
                return Response(util.error(self,"State is Invalid"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class AreaDependentCity(APIView):
    def get(self, request, format=None):
        try:
            city = request.GET.get('city','')
            if CityMaster.objects.filter(id = city):
                cityobj = CityMaster.objects.get(id = city)
                areaobj = AreaMaster.objects.filter(city_master = cityobj)
                serializer=AreaSerializer(areaobj, many=True)
                if serializer.data:
                    return Response(util.success(self,serializer.data))
                else:
                    return Response(util.error(self, 'No Data Found'))
            else:
                return Response(util.error(self,"City is Invalid"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class ZipCodeDependeOnCityArea(APIView):
    def get(self, request, format=None):
        try:
            city = request.GET.get('city','')
            area = request.GET.get('area','')
            if area == '':
                cityobj = CityMaster.objects.get(id = city)
                areaobj = AreaMaster.objects.filter(city_master = cityobj).values_list("id", flat=True)
            else:
                areaobj = AreaMaster.objects.filter(id = area).values_list("id", flat=True)

            zipcodeobj = ZipCodeMaster.objects.filter(area_master__in = areaobj).values('Zipcode').distinct()
            serializer = ZipcodeSerializer(zipcodeobj,many=True)
            if serializer.data:
                return Response(util.success(self,serializer.data))
            else:
                return Response(util.error(self, "Data Not Found"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class DocumentsAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format = None):
        try:
            user,usertype, userprofile=get_user_usertype_userprofile(request,request.user.id)
            files = request.FILES.getlist('files')
            counts = len(files)
            if counts is not None:
                for file in files:
                    filename = file.name
                    maxposition = Document.objects.filter(user = user).aggregate(Max('position'))['position__max']
                    if maxposition is None:
                        maxposition = -1
                    Document.objects.create(user = user, file = file, filename = filename, position = maxposition + 2)
                return Response(util.success(self, "Uploaded files"))
            else:
                return Response(util.error(self,'There is no files in request'))
        except Exception as e:
            return Response(util.error(self,str(e)))
    def get(self, request, format = None):
        try:
            user,usertype, userprofile=get_user_usertype_userprofile(request,request.user.id)
            if user:
                documents = Document.objects.filter(user = user).order_by('-position')
                virtual_list = VirtualOffice.objects.filter(userprofile = userprofile)
                team_list = VirtualOfficeTeam.objects.filter(virtualid__in = virtual_list).values_list('email', flat=False)
                customers = User.objects.filter(email__in = team_list)
                signed_documents = Document.objects.filter(user__in = customers, signed_to = user).order_by('-position')
                documentSerializers = DocumentSerializers(documents, many=True)
                singinedDocumentSerializers = DocumentSerializers(signed_documents, many = True)
                customerSerializers = CustomerListSerializer(customers, many = True)
                return Response(util.success(self, {
                    "documents": documentSerializers.data,
                    "signed_documents": singinedDocumentSerializers.data,
                    "customers":customerSerializers.data
                }))
            else:
                return Response(util.error("User not found"))
        except Exception as e:
            return Response(util.error(self,str(e)))
    def put(self, request, format = None):
        try:
            data = request.data
            if data['share_emails'] is not None:            
                for doc_id in data['share_doc_id']:
                    share_doc = Document.objects.get(id = doc_id)
                    if share_doc.shared == True:
                        share_doc.share_with = data['share_emails']
                        for share_email in data['share_emails']:
                            share_to = User.objects.filter(email = share_email).last()
                            if Document.objects.filter(user = share_to, file = share_doc.file):
                                doc = Document.objects.filter(user = share_to, file = share_doc.file).last()
                                doc.shared = True
                                doc.save()
                            else:
                                maxposition = Document.objects.filter(user = share_to).aggregate(Max('position'))['position__max']
                                if maxposition is None:
                                    maxposition = -1
                                Document.objects.create(share_from = share_doc.user, user = share_to, file = share_doc.file,shared = True, filename = share_doc.filename, position = maxposition + 2)
                        share_doc.save()
                return Response(util.success(self,"Sharing success"))
            else:
                return Response(util.error(self,"Invalid data"))
        except Exception as e:
            return Response(util.error(self,str(e)))
    def delete(self, request, formart = None):
        try:
            data = request.data
            if data['doc_id']:
                if Document.objects.get(id = data['doc_id']):
                    Document.objects.get(id = data['doc_id']).delete()
                    return Response(util.success(self, "Delete success"))
                else:
                    return Response(util.error(self, "Document not found"))
            else:
                return Response(util.error(self, "doc_id not provided"))        
        except Exception as e:
            return Response(util.error(self,str(e)))

class DocumentShareStatusAPI(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, format = None):
        try:
            data = request.data
            if data['is_share'] is not None:
                doc = Document.objects.get(id = data['share_doc_id'])
                doc.shared = data['is_share']
                
                if data['is_share'] == 'False' or data['is_share'] == 'false' or data['is_share'] == 0:
                    if doc.share_with is not None:
                        for share_email in doc.share_with:
                                user = User.objects.filter(email = share_email).last()
                                obj_to_del = Document.objects.filter(user = user, shared = True, file = doc.file).last()
                                obj_to_del.shared = False
                                obj_to_del.save()
                        doc.share_with = []
                doc.save()
                return Response(util.success(self,"Change success"))
            else:
                return Response(util.error(self,"Invalid data"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class ShareDocumentAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format = None):
        try:
            user,usertype, userprofile=get_user_usertype_userprofile(request,request.user.id)
            if user:
                doc_list = Document.objects.filter(user = user, shared = True).order_by('-position')
                # shared_doc= Document.objects.filter(share_with__contains = [user.email])
                sharedDocumentSerializers = ShareDocumentSerializers(doc_list, context = {
                    "user_id":user.id
                    }, many = True)
                return Response(util.success(self, sharedDocumentSerializers.data))
            else:
                return Response(util.error("User not found"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class SignDocumentAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format = None):
        try:
            user,usertype, userprofile=get_user_usertype_userprofile(request,request.user.id)
            if user:
                if request.data["doc_id"] and request.data["file"]:
                    doc_id = request.data["doc_id"]
                    content = request.data["file"]
                    format, filestr = content.split(';base64,')
                    ext = format.split('/')[-1]
                    if Document.objects.filter(id = doc_id):
                        document = Document.objects.get(id = doc_id)
                        filename = 'Signed_' + document.filename
                        file = ContentFile(base64.b64decode(filestr), name = filename)
                        if Document.objects.filter(user = user, signed_to = doc_id):
                            signed_documents = Document.objects.filter(user = user, signed_to = document.share_from).last()
                            signed_documents.filename = filename
                            signed_documents.file = file
                            signed_documents.signed = True
                            signed_documents.save()
                        else:
                            maxposition = Document.objects.filter(signed_to = document.user, signed = True).aggregate(Max('position'))['position__max']
                            if maxposition is None:
                                maxposition = 0
                            Document.objects.create(user = user, signed_to = document.share_from,signed = True, signing =doc_id,  filename = filename, file = file, position = maxposition+1)
                        return Response(util.success(self, "Signing success"))
                    else:
                        return Response(util.error(self,"Document not found"))
                else:
                    return Response(util.error(self,"doc_id and file field not found"))
            else:
                return Response(util.error(self,"User not found"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class DocumentOrderAPI(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, format=None):
        try:
            data = request.data
            if 'after_id' in data and 'before_id' in data:
                after = Document.objects.get(id=data['after_id'])
                before = Document.objects.get(id=data['before_id'])
                after.position = before.position + 1
                after.save()
                return Response(util.success(self,"Order updated"))
            else:
                return Response(util.error(self,"after_id and before_id field required"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class DocTitleRenameAPI(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, format=None):
        try:
            data = request.data
            if 'doc_id' in data and 'title' in data:
                doc = Document.objects.get(id=data['doc_id'])
                doc.filename = data['title']
                doc.save()
                share_doc = Document.objects.filter(file = doc.file).exclude(user = request.user)
                for i in share_doc:
                    i.filename = data['title']
                    i.save()
                return Response(util.success(self,"Title updated"))
            else:
                return Response(util.error(self,"doc_id and title field required"))
        except Exception as e:
            return Response(util.error(self,str(e)))