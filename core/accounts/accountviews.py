import calendar
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import json
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.core import serializers as core_serializers
from django.views.decorators.csrf import csrf_exempt
from .renderers import *
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework.parsers import MultiPartParser, FormParser
import os
from rest_framework import generics, status, views, permissions
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
import jwt
from django.conf import settings
from django.urls import reverse 
from django.contrib.sites.shortcuts import get_current_site
from .utils import Util
from .views import get_user_usertype_userprofile
from property.models import *
from master import util
from django.core.mail import EmailMessage
import uuid
import itertools
# from Crypto.Cipher import AES
import base64
from property.serializer import *
from datetime import date
from virtual_office.serializer import *
from django.db.models import Q
class AccountSettingView(APIView):
    permission_classes= [IsAuthenticated]
    def put(self, request, format=None, id=None):
        try:
            data=request.data
            if 'user_id' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request, data['user_id'])
                # print(user,usertype,userprofile)
                if user:
                    accountsettingobj=AccountSetting.objects.get(user=user)
                    # print(accountsettingobj)
                    if 'type_allowed' in data:
                        accountsettingobj.type_allowed=data['type_allowed']
                    if 'email_notification' in data:
                        accountsettingobj.email_notification=data['email_notification']
                        
                    if 'text_notification' in data:
                        accountsettingobj.text_notification=data['text_notification']
                    
                    accountsettingobj.save()
                    return Response(util.success(self,'Account Settings updated successfully'))
                else:
                    return Response(util.error(self,'User Not Found'))
            else:
                return Response(util.error(self,'user_id needed'))
        except Exception as e:
            return Response(util.error(self,str(e))) 
        
    def get(self, request, format= None,id=None):
        try:
            if id is not None:
                user,usertype, userprofile=get_user_usertype_userprofile(request, id)
                if user:
                    if AccountSetting.objects.filter(user=user.id).exists():
                        accountsettingobj=AccountSetting.objects.get(user=user.id)
                        serializer=AccountSettingSerializer(accountsettingobj)
                        if serializer.data:
                            return Response(util.success(self,serializer.data))
                        else:
                            return Response(util.error(self,"No Data Found"))
                    else:
                        return Response(util.error(self,'Account Settings Not Found'))
                else:
                    return Response(util.error(self,'User not found'))
            else:
                return Response(util.error(self,'user_id is needed'))
        except Exception as e:
            return Response(util.error(self,str(e))) 

class Guest_Users_Save_Listing_View(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format = None):
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
                                guestobj = Guest_Users_Save_Listing.objects.create(user=user, property_details=propertyobj1)
                        return Response(util.success(self,'Property Save'))
                    else:
                        return Response(util.error(self,'Property Not Found'))
                else:
                    return Response(util.error(self,'User Id Not valid'))
            else:
                return Response(util.error(self,'user_id, property_details_id is needed'))
        except Exception as e:
            return Response(util.error(self,str(e))) 

    def get(self, request, format=None , id=None):
        try:
            if id is not None:
                user,usertype, userprofile=get_user_usertype_userprofile(request, id)
                if user:
                    property_detail_obj = Property_Detail.objects.all()
                    if Guest_Users_Save_Listing.objects.filter(user=user.id):
                        GuestUsersSaveListingobj=Guest_Users_Save_Listing.objects.filter(user=user.id).filter(property_details__in  = property_detail_obj)
                        serializer=GuestUsersSaveListingSerializer(GuestUsersSaveListingobj,many=True)
                        if serializer.data:
                            return Response(util.success(self,serializer.data))
                        else:
                            return Response(util.error(self,"No Data Found"))
                    else:
                        return Response(util.error(self,'Guest_Users Id Not Match'))
                else:
                    return Response(util.error(self,'User not found'))
            else:
                allguest=Guest_Users_Save_Listing.objects.filter(user = request.user)
                serializer=GuestUsersSaveListingSerializer(allguest, many=True)
                return Response(util.success(self, serializer.data))
        except Exception as e:
            return Response(util.error(self,str(e))) 

    def delete(self, request, format=None, id= None):
        try:
            if id is not None:
                user_id=request.GET.get('userid','')
                user,usertype, userprofile=get_user_usertype_userprofile(request,user_id)
                if user:
                    savedlistingobj = Guest_Users_Save_Listing.objects.filter(property_details=id).get(user = user)
                    savedlistingobj.delete()
                    return Response(util.success(self,'Unlist Successfully'))
                else:
                    return Response(util.error(self,'User not found'))
            else:
                return Response(util.error(self,'id is needed'))
        except Exception as e:
            return Response(util.error(self,str(e))) 


       
class Delete_User_account(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request, format=None, id=None):
        try:
            user,usertype, userprofile=get_user_usertype_userprofile(request,id)
            if user:
                user.is_active = False
                user.save()
                return Response(util.success(self,'User Deleted Successfully'))
            else:
                return Response(util.error(self,'User not found'))
        except Exception as e:
            return Response(util.error(self,str(e))) 

class Suspend_User_account(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, format=None, id=None):
        try:
            user,usertype, userprofile=get_user_usertype_userprofile(request,id)
            if user:
                if AgentApprovedSubscriptionPlan.objects.filter(user=user):
                    agentobj = AgentApprovedSubscriptionPlan.objects.filter(user=user)
                    for i in agentobj:
                        i.next_billing_date = None
                        i.status = False
                        i.save()
                return Response(util.success(self,'You Plan has stop'))
            else:
                return Response(util.error(self,'User not found'))
        except Exception as e:
            return Response(util.error(self,str(e)))


class AgentUserProfile(APIView):
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated]
    def put(self, request, format=None):
        try:
            user_id = request.POST.get('user_id')
            profile_image=request.FILES.get('profile_image')
            cover_image=request.FILES.get('cover_image')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            nickname=request.POST.get('nickname')
            work_number = request.POST.get('work_number')
            cell_number = request.POST.get('cell_number')
            work_area_id = request.POST.get('work_area_id')
            work_zipcode = request.POST.get('work_zipcode')
            work_city_id = request.POST.get('work_city_id')
            work_state_id = request.POST.get('work_state_id')
            language_speak=request.POST.get('language_speak')
            personal_bio=request.POST.get('personal_bio')
            timezoneobj = request.POST.get('time_zone')
            slug = request.POST.get('slug')
            # return Response("Yess")

            if user_id != None:
                user,usertype,userprofile=get_user_usertype_userprofile(request,user_id)
                if userprofile:
                    if slug:
                        userprofile.slug = slug
                    if profile_image:
                        userprofile.profile_image=profile_image
                    if cover_image:
                        userprofile.cover_image=cover_image
                    if first_name:
                        userprofile.first_name=first_name
                    if last_name:
                        userprofile.last_name=last_name    
                    if nickname:
                        userprofile.nickname=nickname
                    if  work_number:   
                        userprofile.work_number_1=work_number
                    if  cell_number:   
                        userprofile.cell_number=cell_number
                    if language_speak:
                        data=json.loads(language_speak)
                        userprofile.languages=data
                    if timezoneobj:
                        userprofile.time_zone = timezoneobj
                    if  personal_bio:   
                        userprofile.personal_bio=personal_bio
                    if work_zipcode:
                        userprofile.zip_code=work_zipcode
                    if AreaMaster.objects.filter(id=work_area_id):
                        userprofile.areamaster=AreaMaster.objects.get(id=work_area_id)
                    if CityMaster.objects.filter(id=work_city_id):
                        userprofile.citymaster=CityMaster.objects.get(id=work_city_id)
                    if StateMaster.objects.filter(id=work_state_id):
                        userprofile.state=StateMaster.objects.get(id=work_state_id)
                    userprofile.save()
                    # return Response({'msg':'User Profile Updated Successfully'},status=200)
                    return Response(util.success(self,'Saved Successfully'))
                else:
                    # return Response({'msg':'User Profile not found'},status=400)
                    return Response(util.error(self,'User Profile not found'))
            else:
                # return Response({'msg':'user not found'},status=400)
                return Response(util.error(self,'user not found'))
        except Exception as e:
            return Response(util.error(self,str(e))) 

    def get(self, request, format=None, slug=None):
        # try:
            if slug is not None:
                userprofileobjid = UserProfile.objects.get(slug = slug)
                user,usertype, userprofile=get_user_usertype_userprofile(request, userprofileobjid.user_type.user.id)
            else:
                user,usertype, userprofile=get_user_usertype_userprofile(request, request.GET.get('id'))
            if user:
                if userprofile:
                    agentprofile = []
                    usertypeobj = UserTypeSerializer(usertype)
                    unexpired_property=[]
                    expired_property=[]
                    subscription_plan = []
                    agent_license = []
                    nb_area = []
                    languages = []
                    if Property_Detail.objects.filter(user_profile = userprofile):
                        userprofile.listing_count = Property_Detail.objects.filter(user_profile = userprofile).count()
                        userprofile.save()
                        current_list = Property_Detail.objects.filter(user_profile = userprofile, is_property_open=True)
                        unexpired_property=AgentPropertySerializer(current_list, context = {"user_id": request.user}, many=True).data
                        close_list = Property_Detail.objects.filter(user_profile=userprofile).filter(is_property_open=False)
                        expired_property=AgentPropertySerializer(close_list, context = {"user_id": request.user}, many=True).data
                    if AgentApprovedSubscriptionPlan.objects.filter(user = user):
                            agentsubscriptionplan = AgentApprovedSubscriptionPlan.objects.filter(user = user)
                            subscription_plan = AgentApprovedSubscriptionPlanserializer(agentsubscriptionplan,many=True).data
                    if AgentLic.objects.filter(user=user):
                        agentlicobj= AgentLic.objects.get(user=user)
                        agent_license = AgentLicSerializer(agentlicobj).data
                    if Nb_specality_area.objects.filter(user = user):
                        nb_specility_obj = Nb_specality_area.objects.get(user = user)
                        areaobj = AreaMaster.objects.filter(id__in = nb_specility_obj.area_id)
                        nb_area = AreaSerializer(areaobj, many=True).data
                    if AgentProfileSerializer(userprofile):
                        serializer=AgentProfileSerializer(userprofile)
                        agentprofile = serializer.data
                        if serializer.data['languages']:
                            languageobj = LanguageMaster.objects.filter(id__in = serializer.data['languages'])
                            languages = loadLanguageSerializer(languageobj, many=True).data
                    return Response(util.success(self,[agentprofile,user.username,usertypeobj.data,languages,subscription_plan,agent_license,nb_area,unexpired_property,expired_property]))
                else:
                    return Response(util.error(self,'User Id Not Match'))
            else:  
                return Response(util.error(self,'User not found'))
            # else:
            #     return Response(util.error(self,'User Slug needed'))
        # except Exception as e:
        #     return Response(util.error(self,str(e)))



class Teamemeberlanguageandcity(APIView):
    def get(self, request, format=None, slug=None):
        try:
            if slug is not None:
                userprofileobjid = UserProfile.objects.get(slug = slug)
                user,usertype, userprofile=get_user_usertype_userprofile(request, userprofileobjid.user_type.user.id)
                if user:
                    if Nb_specality_area.objects.filter(user = user):
                        obj = Nb_specality_area.objects.get(user = user)
                    else:
                        obj = None
                    if Invitation.objects.filter(userid = user,is_accept=True):
                        invitationobj = Invitation.objects.filter(userid = user,is_accept=True).values_list('email', flat=True)
                        userobj = User.objects.filter(username__in=invitationobj).values_list('id', flat=True)

                        # Area
                        area_id = []
                        language_id = []
                        for i in userobj:
                            usertypeobj = UserType.objects.get(user = i)
                            userprofileobj = UserProfile.objects.get(user_type = usertypeobj)
                            if userprofileobj.languages != None:
                                language_id.append(userprofileobj.languages)
                            if Nb_specality_area.objects.filter(user = i):
                                nbobj = Nb_specality_area.objects.get(user = i)
                                area_id.append(nbobj.area_id)
                        areaobj =  list(set(itertools.chain(*area_id)))
                        languageobj = list(set(itertools.chain(*language_id)))
                        if obj != None:
                            areaobj = [value for value in areaobj if value not in obj.area_id]
                        areaobj1 = AreaMaster.objects.filter(id__in = areaobj)
                        area_serializer = AreaSerializer(areaobj1, many=True)
                        languageobj1 = LanguageMaster.objects.filter(id__in = languageobj)
                        language_serializer = loadLanguageSerializer(languageobj1, many=True)
                        return Response(util.success(self, {"area":area_serializer.data, "language":language_serializer.data}))
                        # if area_serializer.data != None and language_serializer.data != None:
                        #     return Response(util.success(self, {"area":area_serializer.data, "language":language_serializer.data}))
                        # elif area_serializer.data != None and language_serializer.data == None:
                        #     return Response(util.success(self, {"area":area_serializer.data, "language":[]}))
                        # elif area_serializer.data == None and language_serializer.data != None:
                        #     return Response(util.success(self, {"language":language_serializer.data}))
                        # else:
                        #     return Response(util.error(self, 'No Data Found'))

                    else:
                        return Response(util.error(self, 'No user Found'))
                else:  
                    return Response(util.error(self,'User not found'))
            else:
                return Response(util.error(self,'User Slug needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class SocilMediaLink(APIView):
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated]
    def put(self, request, format=None):
        try:
            data=request.data
            if 'user_id' in data :
                user,usertype, userprofile=get_user_usertype_userprofile(request,data['user_id'])
                if userprofile:
                    if "linkedin_url" in data:
                        userprofile.linkedin_url=data['linkedin_url']
                    if "facebook_url" in data:
                        userprofile.facebook_url=data['facebook_url']
                    if "twitter_url" in data:
                        userprofile.twitter_url=data['twitter_url']
                    if "instagram_url" in data:
                        userprofile.instagram_url=data['instagram_url']
                    if "youtube_url" in data:
                        userprofile.youtube=data['youtube_url']
                    if "tictok_url" in data:
                        userprofile.tiktok_url=data['tictok_url']
                    
                    userprofile.save()
                    # return Response({'msg':'User Profile Updated Successfully'},status=200)
                    return Response(util.success(self,'Social Media linked successfully!'))
                else:
                    # return Response({'msg':'User Profile not found'},status=400)
                    return Response(util.error(self,'User Profile not found'))
            else:
                # return Response({'msg':'Userid not found'},status=400)
                return Response(util.error(self,'user_id not found'))
        except Exception as e:
            return Response(util.error(self,str(e))) 

    def get(self, request, format=None, slug=None):
        try:
            if slug is not None:
                userprofileobjid = UserProfile.objects.get(slug = slug)
                user,usertype, userprofile=get_user_usertype_userprofile(request, userprofileobjid.user_type.user.id)
                if user:
                    if userprofile: 
                        usertypeobj = UserTypeSerializer(usertype)
                        serializer=AgentProfileSerializer(userprofile)
                        # print('serializer',serializer)
                        if serializer.data:
                            if AgentLic.objects.filter(user=user):
                                agentlicobj= AgentLic.objects.get(user=user)
                                serializer1 = AgentLicSerializer(agentlicobj)
                                return Response(util.success(self,[serializer.data , user.username, serializer1.data,usertypeobj.data]))
                            else:
                                return Response(util.success(self,[serializer.data, user.username,usertypeobj.data]))
                        else:
                            return Response(util.error(self,"No Data Found"))
                    else:  
                        return Response(util.error(self,'User Id Not Match'))
                else:  
                    return Response(util.error(self,'User not found'))
            else:
                return Response(util.error(self,'Userid needed'))
        except Exception as e:
            return Response(util.error(self,str(e))) 

class Create_Team_Name(APIView):
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated]
    def put(self, request, format=None):
        try:
            data=request.data
            if 'user_id' in data and 'create_team' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['user_id'])
                if user:
                    if data['create_team'] == True:
                        if 'Team_name' in data:
                            userprofile.team_name=data['Team_name']
                            userprofile.create_team=True
                            userprofile.save()
                            return Response(util.success(self, "Team created Successfully!"))
                        else:
                            return Response(util.error(self, 'Team_name is needed'))
                    else:
                        return Response(util.error(self, 'Ok Skip that'))
                else:
                    return Response(util.error(self, 'User Profile not found'))
            else:
                return Response(util.error(self, 'user_id, create_team is needed'))
        except Exception as e:
            return Response(util.error(self,str(e))) 
    
    def delete(self, request, format=None, id=None):
        try:
            if id is not None:
                invite = Invitation.objects.get(id=id)
                invite.delete()
                return Response(util.success(self, 'Invitation Deleted'))
            else:
                return Response(util.error(self,'id needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

    
    def post(self, request, format=None):
        try:
            data=request.data
            if 'user_id' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['user_id'])
                if user:
                    teammember = Invitation.objects.filter(userid=user)
                    serializer = InvitationSerializer(teammember, many=True)
                    if serializer.data:
                        return Response(util.success(self,serializer.data))
                    else:
                        return Response(util.error(self, 'No Data Found'))
                else:
                    return Response(util.error(self, 'User not found'))
            else:
                return Response(util.error(self, 'user_id, is needed'))
        except Exception as e:
            return Response(util.error(self,str(e))) 

class Brokerage_name_license(APIView):
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self, request, format=None):
        try:
            data=request.data
            if 'user_id' in data and 'License_title' in data and 'Brokerage_Name' in data and 'Salespersons_License' in data:
                user,usertype, userprofile=get_user_usertype_userprofile(request,data['user_id'])
                if user and usertype and userprofile.first_name and userprofile.last_name:
                    
                    if AgentLic.objects.filter(user=user).exists():
                        AgentLicObj=AgentLic.objects.get(user=user)
                        AgentLicObj.lic_Type = data['License_title']
                        AgentLicObj.brokerage_name=data['Brokerage_Name']
                        AgentLicObj.license_number=data["Salespersons_License"]
                        AgentLicObj.Full_name = userprofile.first_name+' '+userprofile.last_name
                        AgentLicObj.first_name = userprofile.first_name
                        AgentLicObj.last_name = userprofile.last_name
                        AgentLicObj.is_requested=True
                        AgentLicObj.save()
                        return Response(util.error(self, "Updated Successfully Please Wait for Admin Approval"))
                    else:
                        if AgentLic.objects.filter(license_number=data['Salespersons_License']).exists():
                            AgentLicObj=AgentLic.objects.get(license_number=data['Salespersons_License'])
                            if AgentLicObj.lic_already_use==True:
                                return Response(util.error(self, "This Licence number is alreay In Use"))
                            elif AgentLic.objects.filter(user=user).exists():
                                return Response(util.error(self, "User is already having a license"))
                            else:
                                if userprofile.first_name==AgentLicObj.first_name and userprofile.last_name==AgentLicObj.last_name:
                                    AgentLicObj.is_validated=True
                                    AgentLicObj.lic_Type = data['License_title']
                                    AgentLicObj.brokerage_name = data['Brokerage_Name']
                                    AgentLicObj.is_requested=False
                                    AgentLicObj.lic_already_use=True
                                    AgentLicObj.is_rejected=False
                                    AgentLicObj.user=user
                                    userprofile.brokerage_name=data['Brokerage_Name']
                                    userprofile.sales_persones_license=data['Salespersons_License']
                                    userprofile.agent_broker_license_title=data['License_title']
                                    AgentLicObj.save()
                                    userprofile.save()
                                    date_now = date.today()
                                    if AgentApprovedSubscriptionPlan.objects.filter(user= user):
                                        agentobj = AgentApprovedSubscriptionPlan.objects.filter(user= user)
                                        for i in agentobj:
                                            i.approved_date=date.today() # 2023-03-31
                                            if i.plan_choices == "Monthly":
                                                year = i.approved_date.year
                                                month = i.approved_date.month + 1
                                                if month > 12:
                                                    year += 1
                                                    month = 1
                                                _, days_in_month = calendar.monthrange(year, month)
                                                day = min(i.approved_date.day, days_in_month)
                                                i.next_billing_date = i.approved_date.replace(year=year, month=month, day=day)
                                                # print(i.next_billing_date)
                                            else:
                                                i.next_billing_date = i.approved_date.replace(year=i.approved_date.year + 1)
                                            i.save()
                                    return Response(util.success(self, "Licence Number Approved Successfully"))
                                else:
                                    AgentLicObj.is_requested=True
                                    AgentLicObj.lic_Type = data['License_title']
                                    AgentLicObj.brokerage_name = data['Brokerage_Name']
                                    AgentLicObj.user=user
                                    AgentLicObj.user=user
                                    AgentLicObj.save()
                                    return Response(util.success(self, "License Number waiting For Admin approval"))
                        else:
                            AgentLic.objects.create(lic_Type = data['License_title'],brokerage_name=data['Brokerage_Name'],user=user,license_number=data["Salespersons_License"],Full_name = userprofile.first_name+' '+userprofile.last_name, first_name = userprofile.first_name, last_name = userprofile.last_name ,is_requested=True)
                            return Response(util.success(self, "Licence Number Waiting For Admin Approval"))
                    
                else:
                    return Response(util.success(self, "Profile Not Found"))
            else:
                return Response(util.error(self,'user_id, License_title, Brokerage_Name, Salespersons_License is needed'))
        except Exception as e:
            return Response(util.error(self,str(e))) 

    def get(self, request, format=None, slug=None):
        try:
            if slug is not None:
                userprofileobjid = UserProfile.objects.get(slug = slug)
                user,usertype, userprofile=get_user_usertype_userprofile(request, userprofileobjid.user_type.user.id)
                if user:
                    if userprofile: 
                        serializer=AgentProfileSerializer(userprofile)
                        usertypeobj = UserTypeSerializer(usertype)
                        # print('serializer',serializer)
                        if serializer.data:
                            if AgentLic.objects.filter(user=user):
                                agentlicobj= AgentLic.objects.get(user=user)
                                serializer1 = AgentLicSerializer(agentlicobj)
                                return Response(util.success(self,[serializer.data , user.username, serializer1.data, usertypeobj.data]))
                            else:
                                return Response(util.success(self,[serializer.data, user.username, usertypeobj.data]))
                        else:
                            return Response(util.error(self,"No Data Found"))
                    else:  
                        return Response(util.error(self,'User Id Not Match'))
                else:  
                    return Response(util.error(self,'User not found'))
            else:
                return Response(util.error(self,'Userid needed'))
        except Exception as e:
            return Response(util.error(self,str(e))) 

'''
{
    user_id:1,
    sunday:{"is_available":"True","slot1":{"start_time":"11:00 am","end_time":"12:00 pm"},"slot2":{"start_time":"11:00 am","end_time":"12:00 pm"}},
    monday:{"is_available":False},
    tuesday:{"is_available":False},
    wednesday:{"is_available":False},
    thrusday:{"is_available":"True","slot1":{"start_time":"11:00 am","end_time":"12:00 pm"},"slot2":{"start_time":"11:00 am","end_time":"12:00 pm"}},
    friday:{"is_available":False},
    saturday:{"is_available":"True","slot1":{"start_time":"11:00 am","end_time":"12:00 pm"},"slot2":{"start_time":"11:00 am","end_time":"12:00 pm"}},
}
'''

class min_30_view(APIView):
    # permission_classes=[IsAuthenticated]
    def post(self, request, format = None):
        try:
            data = request.data
            if data["user_id"] != None:
                user,usertype, userprofile=get_user_usertype_userprofile(request, data["user_id"])
                if userprofile:
                    if 'monday' in data and 'tuesday' in data and 'wednesday' in data and 'thrusday' in data and 'friday' in data and 'saturday' in data and 'sunday' in data:
                        min30obj = min_30.objects.create(
                            userprofile=userprofile,
                            Monday= data['monday'],
                            Tuesday= data['tuesday'],
                            Wednesday= data['wednesday'],
                            Thursday= data['thrusday'],
                            Friday= data['friday'],
                            Saturday= data['saturday'],
                            Sunday= data['sunday'],
                            is_active= True,
                        )
                        return Response(util.success(self, "Successfully Added"))
                    else:
                        return Response(util.error(self,'monday, tuesday, wednesday, thrusday, friday, saturday, sunday is required'))
                else:
                    return Response(util.error(self, "Data not found"))
            else:
                return Response(util.error(self, "user_id is required"))
        except Exception as e:
            return Response(util.error(self,str(e))) 
    
    def get(self, request, format = None, slug= None):
        try:
            if slug is not None:
                userprofileobjid = UserProfile.objects.get(slug = slug)
                user,usertype, userprofile=get_user_usertype_userprofile(request, userprofileobjid.user_type.user.id)
                if userprofile:
                    min_30_obj = min_30.objects.filter(userprofile = userprofile).last()
                    serializer = min_30_Serializer(min_30_obj)
                    if serializer.data:
                        return Response(util.success(self, serializer.data))
                    else:
                        return Response(util.error(self, "Data not found"))
                else:
                    return Response(util.error(self, "Data not found"))
            else:
                return Response(util.error(self, "id is required"))
        except Exception as e:
            return Response(util.error(self,str(e)))
    
    def put(self, request, format = None):
        try:
            pass
        except Exception as e:
            return Response(util.error(self,str(e)))
    
    def delete(self, request, format = None, id= None):
        try:
            if id is not None:
                pass
            else:
                return Response(util.error(self, "id is required"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class plan_and_billing(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, format=None, id=None):
        try:
            if id is not None:
                user,usertype, userprofile=get_user_usertype_userprofile(request, id)
                if user:
                    if AgentApprovedSubscriptionPlan.objects.filter(user=user).exists():
                        agentobj = AgentApprovedSubscriptionPlan.objects.filter(user=user)
                        serializer = AgentApprovedSubscriptionPlanserializer(agentobj, many=True)
                        return Response(util.success(self, serializer.data))
                    else:
                        return Response(util.error(self, "No Data Found"))
                else:
                    return Response(util.error(self, "User Not Found"))
            else:
                return Response(util.error(self, "id is required"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class AddIssuePriorityType(APIView):
    def get(self, request, format = None):
        try:
            issues = IssueType.objects.all()
            priorties = IssuePriority.objects.all()
            getissue_serializer = GetIssueSerializer(issues, many = True)
            getpriority_serializer = GetPrioritySerializer(priorties, many = True)
            if getissue_serializer.data:
                if getpriority_serializer.data:
                    return Response(util.success(self, {"Issues":getissue_serializer.data, "Priority":getpriority_serializer.data}))
                else:
                    return Response(util.success(self, {"Issues":getissue_serializer.data, "Priority":getpriority_serializer.data}))
            else:
                return Response(util.error(self, "Data Not Found"))
        except Exception as e:
            return Response(util.error(self,str(e)))

    