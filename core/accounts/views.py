import email
from faulthandler import is_enabled
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
import uuid
from rest_framework import generics, status, views, permissions
import jwt
from django.conf import settings
from django.urls import reverse 
from django.contrib.sites.shortcuts import get_current_site
from .utils import Util
from master.models import *
from master import util
from property.serializer import *
from django.shortcuts import render, redirect
from django.contrib.auth.models import update_last_login
from datetime import date
from virtual_office.models import *
from django.db.models import Q
from itertools import chain
from accounts.paginatorviews import MyPagination


# generating token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def get_user_usertype_userprofile(request,id):
    if User.objects.filter(id=id):
        user=User.objects.get(id=id)
        usertype=UserType.objects.get(user=user)
    
        if UserProfile.objects.filter(user_type=usertype):
            userprofile=UserProfile.objects.get(user_type=usertype)
            return user,usertype, userprofile
        else:
            return user,usertype,False
    else:
        return False,False,False

# Registration
class UserRegistrationsView(APIView):
    def post(self,request,format=None): 
        try:
            body = request.data
            if 'password' in body and 'user_type' in body and 'username':
                        body['email']=body['username']
                        serializer = UserRegistrationSerializer(data = body)
                        if serializer.is_valid(raise_exception = True):   #remove the the raise_exception = True
                            user = serializer.save()
                            UserType.objects.create(user=user,user_type=body['user_type'])
                            AccountSetting.objects.create(user=user)
                            user_data=serializer.data
                            user = User.objects.get(username=user_data['username'])
                            if body['user_type'] == 1:
                                virtualteams = VirtualOfficeTeam.objects.filter(email = user.email)
                                for i in virtualteams:
                                    i.is_status = True
                                    i.save()
                            token = RefreshToken.for_user(user).access_token
                            current_site = get_current_site(request).domain
                            relativeLink = reverse('email-verify')
                            absurl = 'https://dev.api.MLS-tutor.com'+relativeLink+"?token="+str(token)
                            email_body = 'Hi '+user.username + \
                            ' Use the link below to verify your email \n' + absurl
                            data = {'email_body': email_body, 'to_email': user.username,'email_subject': 'Verify your email'}
                            Util.send_email(data)
                            return Response(util.success(self,'Success Check your E-mail for Registration verification'))
                            # status = status.HTTP_201_CREATED)
                            # after the remove the raise_exceptions = True then the that place 
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        
            else:
                return Response(util.error(self,'password, user_type is Required'))
        except Exception as e:
            return Response(util.error(self,str(e))) 

# login 
class UserLoginView(APIView):
    def post(self,request,format=None):
        try:
            obj=request.data
            agent_profile=False
            agentsubscription=False
            add_on=False
            nb_sb=False
            billing = False
            license_approve = False
            virtual_office = False
            type_of_listing = False
            if 'username' in obj and 'password' in obj and 'user_log' in obj:
                if 'action_type' in obj['user_log'] and 'date_time' in obj['user_log'] and 'ip_address' in obj['user_log'] and 'longitude' in obj['user_log'] and 'latitude' in obj['user_log'] and 'mac_address' in obj['user_log'] and 'location' in obj['user_log'] :
                    if User.objects.filter(username=obj['username']):
                        user_object=User.objects.get(username=obj['username'])
                        if user_object.is_superuser is False:
                            user=authenticate(username=user_object.username,password=obj['password'])
                            if user is not None:
                                token = get_tokens_for_user(user)
                                login(request, user)
                                usertypeobj=UserType.objects.get(user=user)
                                
                                User_Log.objects.create(user_type=usertypeobj,action_type=obj['user_log']['action_type'],
                                date_time=obj['user_log']['date_time'],ip_address=obj['user_log']['ip_address'],
                                longitude=obj['user_log']['longitude'],latitude=obj['user_log']['latitude'],
                                mac_address=obj['user_log']['mac_address'],location=obj['user_log']['location'])
                                user, usertype, userprofile=get_user_usertype_userprofile(request, user.id)
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
                                if VirtualOfficeTeam.objects.filter(email = user):
                                    virtual_office = True
                                if userprofile and UserType.objects.filter(user_type=1) and AccountSetting.objects.filter(user=user):
                                    account_setting = AccountSetting.objects.get(user=user)
                                    type_of_listing = account_setting.type_allowed
                                profileserializer = UserProfileSerializer(userprofile)
                                serializer = ProfileImageSerializer(userprofile)
                                return Response(util.success(self,{'user_info':{'id':user.id,'username':user.username,'usertypeobj':usertypeobj.user_type,"agent_profile":agent_profile, "agentsubscription":agentsubscription, "add_on":add_on, "nb_sb":nb_sb, "billing":billing, "license_approve":license_approve, "is_social":user.is_social,"virtual_office":virtual_office,"type_of_listing":type_of_listing},'token':token,'msg':'login Success','profile':profileserializer.data,'image': serializer.data}))
                            else:
                                return Response(util.error(self,'user Not Found'))
                        else:
                            return Response(util.error(self,'Invalid Crenditial'))
                    else:
                        return Response(util.error(self,'user Not Found'))
                else:
                    return Response(util.error(self,'action_type, date_time, ip_address, longitude, latitude, mac_address, location needed'))
            else:
                return Response(util.error(self,'username and password and user_log needed'))
        except Exception as e:
            return Response(util.error(self,str(e))) 

#logout
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# profile
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format = None, id=None):
        try:
            if id is not None:
                user,usertype,userprofile=get_user_usertype_userprofile(request, id)
                if userprofile:
                    if usertype.user_type==1:
                        response={
                                "user":{'id':user.id,'username':user.email},
                                "user_type":{"id":usertype.id,"user_type":usertype.user_type},
                                "profile":{"id":userprofile.id,"first_name":userprofile.first_name,
                                            "last_name":userprofile.last_name,
                                            "work_number1":userprofile.work_number_1,
                                            "is_work_numer_1_valid":userprofile.is_work_numer_1_valid,
                                            "type_of_account":userprofile.type_of_account,
                                            "town":userprofile.citymaster,
                                            "state":userprofile.state_id,
                                            "zipcode":userprofile.zip_code_id,
                                        }
                            }
                        # return Response(response, status = status.HTTP_200_OK)
                        return Response(util.success(self,response))
                    else:
                        pass
                else:
                    response={
                                "user":{'id':user.id,'username':user.email},
                                "user_type":{"id":usertype,"user_type":usertype.user_type},
                                "profile":"profile not created yet"
                            }
                    # return Response(response, status = status.HTTP_200_OK)
                    return Response(util.success(self,response))
            else:
                return Response(util.error(self, "Id is required"))
        except Exception as e:
            return Response(util.error(self,str(e))) 

    def put(self, request, format=None):
        try:
            userobj = request.user
            body = request.data
            user,usertype,userprofile=get_user_usertype_userprofile(request, userobj.id)
            if userprofile:
                if 'first_name' in body and 'last_name' in body and 'phone_number' in body and 'type_of_account' in body and 'town' in body and 'state' in body and 'zipcode' in body:
                    if UserProfile.objects.filter(work_number_1=body['phone_number']):
                        return Response({'msg':"this Phone number is alreay taken"})
                    else:
                        if CityMaster.objects.filter(id = body['town']):
                            cityobj = CityMaster.objects.get(id = body['town'])
                        else:
                            cityobj = None
                        
                        if StateMaster.objects.filter(id = body['state']):
                            stateobj = StateMaster.objects.get(id = body['state'])
                        else:
                            stateobj = None
                        
                        # if ZipCodeMaster.objects.filter(id = body['zipcode']):
                        #     zipobj = ZipCodeMaster.objects.get(id = body['zipcode'])
                        # else:
                        #     zipobj = None
                        userprofile.first_name=body['first_name']
                        userprofile.last_name=body['last_name']
                        userprofile.work_number_1=body['phone_number']
                        userprofile.type_of_account=body['type_of_account']
                        userprofile.citymaster=cityobj
                        userprofile.state_id=stateobj.id
                        userprofile.zip_code_id=body['zipcode']
                        userprofile.save()
                        return Response("Succss")
                else:
                    return Response(util.error(self,'first_name, last_name, phone_number, type_of_account, town, state, zipcode needed'))
            else:
                return Response(util.error(self, 'Invalid User'))
        except Exception as e:
            return Response(util.error(self,str(e))) 

    # def post(self,request):
    #     user = request.user
    #     usertypeobj=UserType.objects.get(user=user)
    #     body=request.data
    #     if 'first_name' in body and 'last_name' in body and 'phone_number' in body and 'type_of_account' in body and 'town' in body and 'state' in body and 'zipcode' in body:
            
    #         if CityMaster.objects.filter(id = body['town']):
    #             cityobj = CityMaster.objects.get(id = body['town'])
    #         else:
    #             cityobj = None
            
    #         if StateMaster.objects.filter(id = body['state']):
    #             stateobj = StateMaster.objects.get(id = body['state'])
    #         else:
    #             stateobj = None
            
    #         if ZipCodeMaster.objects.filter(id = body['zipcode']):
    #             zipobj = ZipCodeMaster.objects.get(id = body['zipcode'])
    #         else:
    #             zipobj = None

    #         if UserProfile.objects.filter(work_number_1=body['phone_number']):
    #             return Response({'msg':"this Phone number is alreay taken"})
    #         else:
    #             UserProfile.objects.create(
    #                 user_type=usertypeobj, first_name=body['first_name'], last_name=body['last_name'], work_number_1=body['phone_number'], 
    #                 type_of_account=body['type_of_account'], citymaster=cityobj, state_id=stateobj.id, zip_code_id=zipobj.id,
    #             )
    #             return Response(util.success(self,'success'))
    #     else:
    #         return Response(util.error(self,'first_name, last_name, phone_number, type_of_account, town, state, zipcode needed'))

# change Password
class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format = None):
        try:
            data=request.data
            if 'user_id' in data:
                if User.objects.filter(id=data['user_id']):
                    user_object=User.objects.get(id=data['user_id'])
                    if user_object.is_social == False:
                        user_object=authenticate(username=user_object.username,password=data['old_password'])
                    else:
                        user_object.is_social=False
                        user_object.save()

                    if user_object is not None:
                        if data["password1"] == data["password2"]:
                            user_object.set_password(data['password1'])
                            user_object.save()
                            return Response(util.success(self,'Password Change Sucessfully'))
                        else:
                            return Response(util.error(self,'Password1 and Password2 Not Matched'))
                    else:
                        return Response(util.error(self,'Old Password is incorrect')) 
                else:
                    return Response(util.error(self,'user id is not valid'))
            else:
                return Response(util.error(self,'user_id is required'))
        except Exception as e:
            return Response(util.error(self,str(e))) 

#Add or change ProfilePicture
class ChangeProfilePictureView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def put(self, request, format = None):
        try:
            user= request.user
            usertypeobj=UserType.objects.get(user=user)
            if request.FILES.get("image", None) is not None:
                    img = request.FILES["image"]
                    if UserProfile.objects.filter(user_type=usertypeobj):
                        userprofileobj=UserProfile.objects.get(user_type=usertypeobj)
                    else:
                        # return Response({'msg':"UserProfile id is invalid"})
                        return Response(util.error(self,'UserProfile id is invalid'))
                    userprofileobj.profile_image=img
                    userprofileobj.save()
                    # return Response({'msg':"profile image updated"})
                    return Response(util.success(self,'profile image updated'))
            else:   
                # return Response({'msg':"Profile image not found"})
                return Response(util.error(self,'Profile image not found'))
        except Exception as e:
            return Response(util.error(self,str(e))) 

class VerifyEmail(APIView):
    def get(self, request):
        try:
            token = request.GET.get('token')
            try:
                payload = jwt.decode(token, settings.SECRET_KEY,algorithms=['HS256'])
                user = User.objects.get(id=payload['user_id'])
                if not user.is_email_verified:
                    user.is_email_verified = True
                    user.is_active = True
                    user.save()
                    if UserType.objects.filter(user=user):
                        usertypeobj=UserType.objects.get(user=user)
                        if usertypeobj.user_type == 0:
                            UserProfile.objects.create(user_type=usertypeobj, unique_id="Ad")
                        elif usertypeobj.user_type == 1:
                            UserProfile.objects.create(user_type=usertypeobj, unique_id="Gu")
                        elif usertypeobj.user_type == 2:
                            UserProfile.objects.create(user_type=usertypeobj, unique_id="Ag")
                        elif usertypeobj.user_type == 3:
                            UserProfile.objects.create(user_type=usertypeobj, unique_id="Inv/Dev")
                        elif usertypeobj.user_type == 4:
                            UserProfile.objects.create(user_type=usertypeobj, unique_id="FS")
                        else:
                            UserProfile.objects.create(user_type=usertypeobj, unique_id="Ma")
                return redirect(f'{settings.SITE_URL}login')
                # return redirect('http://MLS-tutor.leocoders.com/login')
            
            except jwt.ExpiredSignatureError as identifier:
                return Response(util.error(self,'Activation Expired'))

            except jwt.exceptions.DecodeError as identifier:
                return Response(util.error(self,'Invalid token'))
        except Exception as e:
            return Response(util.error(self,str(e))) 

from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class ForgetPassword(APIView):
    def post(self, request, format= None):
        try:
            email = request.data.get("email")
            if email is not None:
                if User.objects.filter(email=email).exists():
                    user = User.objects.get(email=email)
                    uid = urlsafe_base64_encode(force_bytes(user.id))
                    token = PasswordResetTokenGenerator().make_token(user)
                    absurl = settings.SITE_URL+'reset-password/'+"?uid="+uid+'&'+"token="+token
                    email_body = 'Hi '+user.email + \
                    ' Use the link below to reset your password \n' + absurl
                    data = {'email_body': email_body, 'to_email': user.email,'email_subject': 'Verify your email'}
                    Util.send_email(data)
                    return Response(util.success(self,'Email Sent Successfull'))
                else:
                    return Response(util.error(self,'User Not Found'))
            else:
                return Response(util.error(self, "email is required"))
        except Exception as e:
            return Response(util.error(self,str(e))) 

class ResetPassword(APIView):
    def post(self, request, format=None):
        try:
            uid = request.data.get('uid')
            token = request.data.get('token')
            password = request.data.get('password')
            password1 = request.data.get('password1')
            if password and password1 != None:
                if password != password1:
                    return Response(util.error(self, "Password and Confirm Password doesn't match"))
                id = smart_str(urlsafe_base64_decode(uid))
                user = User.objects.get(id=id)
                if not PasswordResetTokenGenerator().check_token(user, token):
                    return Response(util.error(self,'Token is not Valid or Expired'))
                user.set_password(password)
                user.save()
                return Response(util.success(self,'Password Updated Successfully'))
            else:
                return Response(util.error(self,'password and password1 is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class GuestUserProfile(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def put(self, request, format= None):
        try:
            user_id = request.POST.get('user_id')
            profile_image=request.FILES.get('profile_image')
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            phone_number=request.POST.get('cell_number')
            home_address=request.POST.get('home_address')
            state_id=request.POST.get('state_id')
            zip_code=request.POST.get('zip_code_id')
            if user_id !=None:
                user,usertype,userprofile=get_user_usertype_userprofile(request,user_id)
                if userprofile:
                    if profile_image!=None:
                        userprofile.profile_image=profile_image
                    if first_name!=None:
                        userprofile.first_name=first_name
                    if last_name!=None:
                        userprofile.last_name=last_name
                    if phone_number!=None:
                        userprofile.cell_number=phone_number
                    if home_address!=None:
                        userprofile.address_line_1=home_address
                    if state_id!=None:
                        if StateMaster.objects.filter(id=state_id):
                            userprofile.state=StateMaster.objects.get(id=state_id)
                    if customer_info.objects.filter(email=user.email, is_edit = False):
                            customobjs = customer_info.objects.filter(email=user.email, is_edit = False)
                            for customobj in customobjs:
                                customobj.contact_no_1 = phone_number
                                customobj.name = first_name+' '+last_name
                                customobj.current_address = home_address
                                customobj.is_edit = True
                                customobj.save()
                    userprofile.zip_code=zip_code
                    userprofile.save()
                    return Response(util.success(self,"Profile Updated Successfully"))
                else:
                    return Response(util.error(self,'Profile Not Found'))
            else:
                return Response(util.error(self,'User Not Found'))
        except Exception as e:
            return Response(util.error(self,str(e))) 


    def get(self, request, format=None, id=None):
        try:
            if User.objects.filter(id=id):
                userobj=User.objects.get(id=id)
                if UserType.objects.filter(user=userobj.id):
                    usertypeobj=UserType.objects.get(user=userobj.id)
                    if UserProfile.objects.filter(user_type=usertypeobj):
                        userprofileobj=UserProfile.objects.get(user_type=usertypeobj)
                        serializer=UserProfileSerializer(userprofileobj)
                        if serializer.data:
                            return Response(util.success(self,serializer.data))
                        else:
                            return Response(util.error(self,"No Data Found"))
                    else:
                        return Response(util.error(self,'User id is not valid'))
                else:
                    return Response(util.error(self,'User id is not valid'))
            else:
                return Response(util.error(self,'User id is not valid'))
        except Exception as e:
            return Response(util.error(self,str(e))) 

class AgentApprovedSubscriptionPlanView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request, format=None):
        try:
            data=request.data
            if "user_id" in data and "subscription_plan_id" in data and "requested_date" in data and 'plan_choices' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(self, data["user_id"])
                if user:
                    if AgentApprovedSubscriptionPlan.objects.filter(user=user).exists():
                        Agent_plan=AgentApprovedSubscriptionPlan.objects.filter(user=user)
                        for item in Agent_plan:
                            item.delete()

                        for i in data["subscription_plan_id"]:
                            if SubscriptionPlanServices.objects.filter(id=i):
                                subscriptionplanobj=SubscriptionPlanServices.objects.get(id=i)
                                AgentApprovedSubscriptionPlan.objects.create(user=user,plan_id=subscriptionplanobj,requested_date=data["requested_date"], plan_choices=data["plan_choices"])
                        return Response(util.success(self,"Agent Plan Re-Created Successfully"))
                        
                    else:
                        for i in data["subscription_plan_id"]:
                            if SubscriptionPlanServices.objects.filter(id=i):
                                subscriptionplanobj=SubscriptionPlanServices.objects.get(id=i)
                                AgentApprovedSubscriptionPlan.objects.create(user=user,plan_id=subscriptionplanobj,requested_date=data["requested_date"], plan_choices=data["plan_choices"])
                        return Response(util.success(self,"Agent Plan Created Successfully"))
                else:
                    return Response(util.error(self,"user_id is not valid"))
            else:
                return Response(util.error(self,"user_id needed,subscription_plan_id,plan_choices and requested_date is needed"))
        except Exception as e:
            return Response(util.error(self,str(e))) 

class AgentApprovedSubscriptionplanchoices(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request, format=None):
        try:
            data=request.data
            if "user_id" in data:
                user,usertype,userprofile=get_user_usertype_userprofile(self, data["user_id"])
                if AgentApprovedSubscriptionPlan.objects.filter(user=user,plan_choices="Yearly"):
                    agentapprovedsubscriptionplanobj=AgentApprovedSubscriptionPlan.objects.filter(user=user).filter(plan_choices="Yearly")
                    l=[]
                    for i in agentapprovedsubscriptionplanobj:
                        l.append(i.plan_id.id)
                        # print(l)
                    obj=SubscriptionPlanServices.objects.filter(id__in=l)
                    # price=[]
                    # for j in obj:
                    #     price.append(j.yearly_price)
                    # # print(price)
                    # return Response(util.success(self,"Yearly Plan Choice Successfully"))
                    plan={}
                    for j in obj:
                        plan[j.Name]=j.monthly_price
                    # print(plan)
                    total=sum(plan.values())
                    return Response(util.success(self,[{"plan":plan},{"total":total}]))
                else:
                    agentapprovedsubscriptionplanobj=AgentApprovedSubscriptionPlan.objects.filter(user=user).filter(plan_choices="Monthly")
                    # print(agentapprovedsubscriptionplanobj)
                    l=[]
                    for i in agentapprovedsubscriptionplanobj:
                        l.append(i.plan_id.id)
                    obj=SubscriptionPlanServices.objects.filter(id__in=l)
                    plan={}
                    for j in obj:
                        plan[j.Name]=j.monthly_price
                    # print(plan)
                    total=sum(plan.values())
                    return Response(util.success(self,[{"plan":plan},{"total":total}]))
            else:
                return Response(util.error(self,"user_id is not valid")) 
        except Exception as e:
            return Response(util.error(self,str(e)))              

class AgentDashboardWithListingType(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            data=request.data
            if "user_id" in data:
                user,usertype,userprofile=get_user_usertype_userprofile(self,data["user_id"])
                obj=AgentApprovedSubscriptionPlan.objects.filter(user=user) 
                SubscriptionPlanServicesobj=None
                for i in obj:
                    if i.plan_id.plan_type == "Regular":
                        SubscriptionPlanServicesobj=i.plan_id

                if SubscriptionPlanServicesobj !=None:
                    if SubscriptionPlanServicesobj.listing_type == 0:
                        if Propertylisting_type.objects.filter(property_listing_name="Residential"): 
                            propertyobj=Propertylisting_type.objects.get(property_listing_name="Residential")
                            propetytypeobj=Property_Listing_Type.objects.filter(type_of_listing=propertyobj)
                            if AgentLic.objects.filter(user=user):
                                agentlicobj=AgentLic.objects.get(user=user)
                                if agentlicobj.is_validated==True:
                                    serialize=Property_listing_typeViewSerializer(propetytypeobj, many=True)
                                    if serialize.data:
                                        return Response(util.success(self,[serialize.data,{"license_is_valid":True, 'Subscription':SubscriptionPlanServicesobj.listing_type}]))
                                    else:
                                        return Response(util.error(self,"No data found."))
                                else:
                                    serialize=Property_listing_typeViewSerializer(propetytypeobj, many=True)
                                    if serialize.data:
                                        return Response(util.success(self,[serialize.data,{"license_is_valid":False, 'Subscription':SubscriptionPlanServicesobj.listing_type}]))
                                    else:
                                        return Response(util.error(self,"No data found."))
                            else:
                                serialize=Property_listing_typeViewSerializer(propetytypeobj, many=True)
                                if serialize.data:
                                    return Response(util.success(self,[serialize.data,{"license_is_valid":False,'Subscription':SubscriptionPlanServicesobj.listing_type}]))
                                else:
                                    return Response(util.error(self,"No data found."))
                        else:
                            return Response(util.error(self,"Please add Residential in Propertylisting_type"))
                    
                    
                    elif SubscriptionPlanServicesobj.listing_type == 1:
                        if Propertylisting_type.objects.filter(property_listing_name="Commercial"): 
                            propertyobj=Propertylisting_type.objects.get(property_listing_name="Commercial")
                            propetytypeobj=Property_Listing_Type.objects.filter(type_of_listing=propertyobj)
                            if AgentLic.objects.filter(user=user):
                                agentlicobj=AgentLic.objects.get(user=user)
                                if agentlicobj.is_validated==True:
                                    serialize=Property_listing_typeViewSerializer(propetytypeobj, many=True)
                                    if serialize.data:
                                        return Response(util.success(self,[serialize.data,{"license_is_valid":True,'Subscription':SubscriptionPlanServicesobj.listing_type}]))
                                    else:
                                        return Response(util.error(self,"No data found."))
                                else:
                                    serialize=Property_listing_typeViewSerializer(propetytypeobj, many=True)
                                    if serialize.data:
                                        return Response(util.success(self,[serialize.data,{"license_is_valid":False,'Subscription':SubscriptionPlanServicesobj.listing_type}]))
                                    else:
                                        return Response(util.error(self,"No data found."))
                            else:
                                serialize=Property_listing_typeViewSerializer(propetytypeobj, many=True)
                                if serialize.data:
                                    return Response(util.success(self,[serialize.data,{"license_is_valid":False, 'Subscription':SubscriptionPlanServicesobj.listing_type}]))
                                else:
                                    return Response(util.error(self,"No data found."))
                        else:
                            return Response(util.error(self,"Please add Residential in Propertylisting_type"))
                    
                    elif SubscriptionPlanServicesobj.listing_type == 2:
                            propetytypeobj=Property_Listing_Type.objects.all()
                            serialize=Property_listing_typeViewSerializer(propetytypeobj, many=True)
                            if serialize.data:
                                return Response(util.success(self,[serialize.data,{'Subscription':SubscriptionPlanServicesobj.listing_type}]))
                            else:
                                return Response(util.error(self,"No data found."))
                    
                else:
                    propetytypeobj=Property_Listing_Type.objects.all()
                    serialize=Property_listing_typeViewSerializer(propetytypeobj, many=True)
                    if serialize.data:
                        return Response(util.success(self,[serialize.data,{'Subscription':SubscriptionPlanServicesobj}]))
                    else:
                        return Response(util.error(self,"No data found."))
            
            else:
                return Response(util.error(self,"user_id needed"))
        except Exception as e:
            return Response(util.error(self,str(e))) 

# class Neighborhood_Specialist_Area_Saved(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self, request, format=None):
#         user=request.POST.get('user')
#         area_id=request.POST.getlist('area_id')
#         doc1=request.FILES.get('doc1')
#         doc2=request.FILES.get('doc2')
#         doc3=request.FILES.get('doc3')
#         if user is not None:
#             user, usertype, userprofile=get_user_usertype_userprofile(request, user)
#             for number in area_id[0].split(','):
#                 areaobj = AreaMaster.objects.get(id=int(number))
#                 obj=Nb_specality_area.objects.create(user=user,area_id=areaobj, doc1=doc1, doc2=doc2, doc3=doc3)
#             return Response(util.success(self,'Saved Sucessfully')) 
#         else:
#             return Response(util.error(self, 'user is required'))

class Neighborhood_Specialist_Area_Saved(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            user=request.POST.get('user')
            area_id=request.POST.get('area_id')
            doc1=request.FILES.get('doc1')
            doc2=request.FILES.get('doc2')
            doc3=request.FILES.get('doc3')
            if user is not None:
                user, usertype, userprofile=get_user_usertype_userprofile(request, user)
                data=json.loads(area_id)
                if Nb_specality_area.objects.filter(user=user):
                    neighborhoodobj = Nb_specality_area.objects.filter(user=user).delete()
                    # neighborhoodobj.delete()
                obj=Nb_specality_area.objects.create(user=user,area_id=data, doc1=doc1, doc2=doc2, doc3=doc3,is_requested = True)
                return Response(util.success(self,'Saved Successfully !')) 
            else:
                return Response(util.error(self, 'user is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))
    
    def get(self, request, format=None, slug=None):
        try:
            if slug is not None:
                userprofileobjid = UserProfile.objects.get(slug = slug)
                user, usertype, userprofile=get_user_usertype_userprofile(request, userprofileobjid.user_type.user.id)
                if user:
                    if Nb_specality_area.objects.filter(user=user):
                        neighborhoodobj = Nb_specality_area.objects.get(user=user)
                        serializer = NeighborhoodSpecilityAreaSerializer(neighborhoodobj)
                        return Response(util.success(self,serializer.data))
                    else:
                        return Response(util.error(self, "No data Found"))
                else:
                    return Response(util.error(self, "user not found"))
            else:
                return Response(util.error(self, "id is required"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class SupportTicketView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            user=request.POST.get('user')
            ticket_no=uuid.uuid4()
            ticket_no_shrt= ticket_no.time_low
            ticket_no_final=hex(int(ticket_no_shrt))[2:]
            issue_type=request.POST.get('issue_type')
            title=request.POST.get('title')
            description=request.POST.get('description')
            priority=request.POST.get('priority')
            image=request.FILES['image']
            status=request.POST.get('status')
            reported_date=request.POST.get('reported_date')
            comments=request.POST.get('comments')

            if user !=  None:
                user, usertype, userprofile=get_user_usertype_userprofile(request, user)
                if user:
                    SupportTickets.objects.create(user=user,ticket_no=ticket_no_final, issue_type=issue_type, title=title, description=description, priority=priority, image=image, status=status,reported_date=reported_date,comments=comments)    
                    return Response(util.success(self,'SupportTicket generation successfully'))
                else:
                    return Response(util.error(self,'user data not found')) 
            else:
                return Response(util.error(self,'user is nedded')) 
        except Exception as e:
            return Response(util.error(self,str(e))) 

    # def put(self, request, format=None):
    #     user=request.POST.get('user')
    #     ticket_no=request.POST.get('ticket_no')
    #     issue_type=request.POST.get('issue_type')
    #     title=request.POST.get('title')
    #     description=request.POST.get('description')
    #     priority=request.POST.get('priority')
    #     image=request.FILES['image']
    #     status=request.POST.get('status')
    #     # print("user",user)
    #     if user != "":
    #         user,usertype,userprofile=get_user_usertype_userprofile(request,user)
    #         if user:
    #             if SupportTickets.objects.filter(id=id):
    #                 supportticketobj=SupportTickets.objects.get(id=id)
    #                 # print(supportticketobj)
    #             else:
    #                 supportticketobj=None

    #             if supportticketobj!=None:
                
    #                 issue_type=request.POST.get('issue_type')
    #                 if issue_type!=None:
    #                     supportticketobj.issue_type=issue_type
    #                     # print(issue_type)

    #                 title=request.POST.get('title')     
    #                 if title!=None:
    #                     supportticketobj.title=title

    #                 description=request.POST.get('description')   
    #                 if description!=None:
    #                     supportticketobj.description=description

    #                 priority=request.POST.get('priority')
    #                 if priority!=None:
    #                     supportticketobj.priority=priority

    #                 image=request.FILES['image']
    #                 if image!=None:
    #                     supportticketobj.image=image

    #                 status=request.POST.get('status')
    #                 if status!=None:
    #                     supportticketobj.status=status

    #                     supportticketobj.save()
    #                 return Response(util.success(self,'SupportTicket edit successful'))
    #             else:
    #                 return Response(util.error(self,'SupportTicket not found'))
    #         else:
    #             return Response(util.error(self,'user data not found')) 
    #     else:
    #         return Response(util.error(self,'user id needed'))        

    def get(self, request, format=None, id=None):
        try:
            if SupportTickets.objects.filter(user=id):
                userobj=SupportTickets.objects.filter(user=id)   
                serializer=SupportticketSerializer(userobj,many=True)
                if serializer.data:
                    return Response(util.success(self,serializer.data))
                else:
                    return Response(util.error(self,'Data Not Found'))
            else:        
                return Response(util.error(self,'Id is nedded'))
        except Exception as e:
            return Response(util.error(self,str(e))) 

    def delete(self, request, format=None, id=None):
        try:
            if id != None:
                user,usertype,userprofile=get_user_usertype_userprofile(request,id)
                # print(user,usertype,userprofile)
                if SupportTickets.objects.filter(id=id):
                    supportticketobj=SupportTickets.objects.get(id=id)
                    supportticketobj.delete()
                    return Response(util.success(self,' Support Ticket deleted successfully'))
                else:
                    return Response(util.error(self,'Supportticket_id is invalid'))
            else:
                    return Response(util.error(self,'Id is invalid'))
        except Exception as e:
            return Response(util.error(self,str(e))) 

class AgentLicView(APIView):
    def get(self, request, format=None, id=None):
        try:
            if id is not None:
                user,usertype,userprofile=get_user_usertype_userprofile(request,id)
                # print(user,usertype,userprofile)
                if user:
                    if AgentLic.objects.filter(user=user):
                        agentlicobj=AgentLic.objects.get(user=user)
                        # print(agentlicobj)
                        serializer=AgentLicSerializer(agentlicobj)
                        if serializer.data:
                            return Response(util.success(self,serializer.data))
                        else:
                            return Response(util.error(self,"No Data Found"))
                    else:
                        return Response(util.success(self,' id needed'))   
                else:
                    return Response(util.error(self,' id needed'))
            else:
                return Response(util.error(self,' id needed'))
        except Exception as e:
            return Response(util.error(self,str(e))) 
            
# import datetime
# from dateutil.relativedelta import relativedelta
# from datetime import datetime, date, timedelta
# class AdminApprovedAgentSubscriptionPlan(APIView):
#     def post(self, request, format=None):
#         approveddate =  datetime.date.today()
#         # print(approveddate)
#         nextbillingdate= approveddate + relativedelta(months=1)   
#         # print(nextbillingdate) 
#         AgentApprovedSubscriptionPlan.objects.create(approved_date=approveddate, next_billing_date=nextbillingdate)
#         return Response(util.success(self,' AdminApprovedAgentSubscriptionPlan is successfully'))

from .profilepasswordviews import encrypt
key = '01234567890123456789015545678901'

class card_create(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            data=request.data
            if 'user_id' in data and 'card_name' in data and 'card_number' in data and 'expirary_date' in data and 'cvv' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['user_id'])
                if user:
                    Expirary_date=data['expirary_date'].split('/')
                    mm=int(Expirary_date[0])
                    yy=int(Expirary_date[1])
                    cvv=encrypt(key, str(data['cvv']))
                    if Card.objects.filter(card_number=data['card_number']):
                        return Response(util.error(self,'Card is Already exits'))
                    else:
                        cardobj=Card.objects.create(user=user,card_number=data['card_number'],
                        card_name=data['card_name'],month=mm,year=yy,cvc=cvv)
                        return Response(util.success(self, "Card added Successfully!"))
                else:
                    return Response(util.error(self,'user not found'))
            else:
                return Response(util.error(self, 'user_id, card_name, card_number, expirary_date, cvv is required '))
        except Exception as e:
            return Response(util.error(self,str(e))) 
    
    def put(self, request, format=None):
        try:
            data = request.data
            if 'user_id' in data and 'card_id' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['user_id'])
                if user:
                    cardobj=Card.objects.get(id=data['card_id'])
                    if data['card_name'] is not None:
                        cardobj.card_name=data['card_name']
                    if data['card_number'] is not None:
                        cardobj.card_number=data['card_number']
                    if data['expirary_date'] is not None:
                        Expirary_date=data['expirary_date'].split('/')
                        mm=int(Expirary_date[0])
                        yy=int(Expirary_date[1])
                        cardobj.month=mm
                        cardobj.year=yy
                    if data['cvv'] is not None:
                        cvv=encrypt(key, str(data['cvv']))
                        cardobj.cvc=cvv
                    cardobj.save()
                    return Response(util.success(self, 'Card updated successfully'))
                else:
                    return Response(util.error(self,'user not found'))
            else:
                return Response(util.error(self, 'user_id, card_id is required'))
        except Exception as e:
            return Response(util.error(self,str(e))) 

    def delete(self, request, format=None, id=None):
        try:
            if id is not None:
                if Card.objects.filter(id=id):
                    cardobj=Card.objects.get(id=id)
                    cardobj.delete()
                    return Response(util.success(self,'card is deleted succesfully'))
                return Response(util.error(self, 'Card Data Not found'))
            return Response(util.error(self, 'Id Is Required'))
        except Exception as e:
            return Response(util.error(self,str(e)))
    
    def get(self, request, format=None, id=None):
        try:
            if id is not None:
                user,usertype,userprofile=get_user_usertype_userprofile(request,id)
                if user:
                    cardobj=Card.objects.filter(user=user)
                    serializer = CardSerializer(cardobj, many=True)
                    if serializer.data:
                        return Response(util.success(self,serializer.data))
                    else:
                        return Response(util.error(self,"No Data Found"))
                else:
                    return Response(util.error(self,'user not found'))
            else:
                return Response(util.error(self, 'id is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))   

class billing(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, format=None):
        try:
            agent_profile=False
            agentsubscription=False
            add_on=False
            nb_sb=False
            data = request.data
            if 'user_id' in data and 'card_id' in data and 'first_name' in data and 'last_name' in data and 'phone_number' in data and 'address_line_1' in data and 'town' in data and 'total_amount' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['user_id'])
                if user:
                    cardobj=Card.objects.get(id=data['card_id'])
                    cityobj=CityMaster.objects.get(id=data['town'])
                    billingobj=Billing.objects.create(
                        user=user,card_id=cardobj,First_Name=data['first_name'],Last_Name=data['last_name'],Phone_number=data['phone_number'],Address1=data['address_line_1'],
                        cityid=cityobj,Total_amount=str(data['total_amount']),payment_date = date.today()
                    )
                    if "address_line_2" in data:
                        if data['address_line_2'] is not None:
                            billingobj.Address2=data['address_line_2']
                        else:
                            pass
                    if "state" in data:
                        if data['state'] is not None:
                            if StateMaster.objects.filter(id=data['state']):
                                sateobj=StateMaster.objects.get(id=data['state'])
                            else:
                                sateobj = None
                            billingobj.stateid=sateobj
                        else:
                            pass
                    if "zipcode" in data:
                        if data['zipcode'] is not None:
                        # zipobj=ZipCodeMaster.objects.get(id=data['zipcode'])
                            billingobj.zipcodeid=data['zipcode']
                        else:
                            pass
                    billingobj.save()
                    if userprofile and AgentLic.objects.filter(user=user).exists():
                        agent_profile=True
                    if AgentApprovedSubscriptionPlan.objects.filter(user=user).exists():
                        agentsubscription=True
                        if AgentApprovedSubscriptionPlan.objects.filter(user=user).count()>1:
                            add_on=True
                    if add_on == True and Nb_specality_area.objects.filter(user=user).exists():
                        nb_sb=True
                    return Response(util.success(self, ['Success! Billing Information is Created Successfully',{"agent_profile":agent_profile, "agentsubscription":agentsubscription, "add_on":add_on, "nb_sb":nb_sb}]))
                else:
                    return Response(util.error(self,'user not found'))
            else:
                return Response(util.error(self,'user_id, card_id, first_name, last_name, phone_number, address1, cityid, total_amount is required'))
        except Exception as e:
            return Response(util.error(self,str(e))) 
    
    def get(self, request, format=None, id=None):
        try:
            if id is not None:
                user,usertype,userprofile=get_user_usertype_userprofile(request,id)
                if user:
                    payment_history = {}
                    agentobj = AgentApprovedSubscriptionPlan.objects.filter(user=user)
                    for i in agentobj:
                        if i.plan_id.Name == "Neighborhood Specialist":
                            subscription = SubscriptionPlanServices.objects.filter(id = i.plan_id.id).exclude(Name="Neighborhood Specialist")
                            for i in subscription:
                                payment_history["Plan_Name"] = i.Name
                            payment_history["Neighborhood"] = "Yes"
                        else:
                            payment_history["Plan_Name"] = i.plan_id.Name
                            payment_history["Neighborhood"] = "No"
                        
                    billingobj = Billing.objects.filter(user=user)
                    for i in billingobj:
                        payment_history['payment_date']=i.payment_date
                        payment_history['Amount']=i.Total_amount
                    return Response(util.success(self,[payment_history]))
                else:
                    return Response(util.error(self, 'User Not Found'))
            else:
                return Response(util.error(self, 'id is required'))
        except Exception as e:
            return Response(util.error(self,str(e))) 

class SocialMedia_Login_Signup_Api(APIView):
    def post(self,request):
        try:
            data=request.data            
            email=data.get('email',None)            
            name=data.get('name','')           
            name_list=name.split()
            agent_profile=False
            agentsubscription=False
            add_on=False
            nb_sb=False
            billing = False
            license_approve = False         
            if email is not None:                
                if User.objects.filter(email=email).exists():
                    
                    user=User.objects.get(email=email)
                    if user.is_active == True:
                        update_last_login(None,user)                            
                        refresh = get_tokens_for_user(user)
                        
                        user, usertype, userprofile=get_user_usertype_userprofile(request, user.id)
                        User_Log.objects.create(user_type=usertype,action_type=data['user_log']['action_type'],
                        date_time=data['user_log']['date_time'],ip_address=data['user_log']['ip_address'],
                        longitude=data['user_log']['longitude'],latitude=data['user_log']['latitude'],
                        mac_address=data['user_log']['mac_address'],location=data['user_log']['location'])
                        
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
                        return Response(util.success(self,{'user_info':{'id':user.id,'username':user.username,'usertypeobj':usertype.user_type,"agent_profile":agent_profile, "agentsubscription":agentsubscription, "add_on":add_on, "nb_sb":nb_sb, "billing":billing, "license_approve":license_approve, "is_social":user.is_social},'token':refresh,'msg':'login Success','profile':profileserializer.data,'image': serializer.data}))
                        # data = {}                            
                        # data['token'] = dict()                            
                        # data['token']['refresh'] = str(refresh)                            
                        # data['token']['access'] = str(refresh.access_token)                            
                        # serializer = UserLoginSerializer(user)                            
                        # data['userData'] = serializer.data                            
                        # # print("data",data)                            
                        # return Response(util.success(self,{'user_info':{'id':user.id,'username':user.username,'usertypeobj':usertype.user_type,"agent_profile":agent_profile, "agentsubscription":agentsubscription, "add_on":add_on, "nb_sb":nb_sb, "billing":billing, "license_approve":license_approve},'token':refresh,'msg':'login Success','profile':profileserializer.data,'image': serializer.data}))                 
                    else:                        
                        return Response(util.error(self,"You are not verified yet please verify your email first"))
                else:
                    
                    if "user_type" in data:               
                        user=User.objects.create_user(username = email,
                                                        email=email,                                                
                                                        first_name=name_list[0],                                                
                                                        last_name=name_list[1],                                                
                                                        is_social=True,
                                                        is_email_verified = True         
                                                    )                    
                        user.is_active = True                    
                        user.is_admin = False                    
                        user.save()

                        usertype = UserType.objects.create(user=user,user_type=data['user_type'])
                        if usertype.user_type == 0:
                            userprofile = UserProfile.objects.create(user_type=usertype, unique_id="Ad")
                        elif usertype.user_type == 1:
                            userprofile = UserProfile.objects.create(user_type=usertype, unique_id="Gu")
                        elif usertype.user_type == 2:
                            userprofile = UserProfile.objects.create(user_type=usertype, unique_id="Ag")
                        elif usertype.user_type == 3:
                            userprofile = UserProfile.objects.create(user_type=usertype, unique_id="Inv/Dev")
                        elif usertype.user_type == 4:
                            userprofile = UserProfile.objects.create(user_type=usertype, unique_id="FS")
                        else:
                            userprofile = UserProfile.objects.create(user_type=usertype, unique_id="Ma")
                        
                        AccountSetting.objects.create(user=user)  
                        update_last_login(None,user)                    
                        refresh = get_tokens_for_user(user)
                        # print("usertype",usertype)
                        User_Log.objects.create(user_type=usertype,action_type=data['user_log']['action_type'],
                        date_time=data['user_log']['date_time'],ip_address=data['user_log']['ip_address'],
                        longitude=data['user_log']['longitude'],latitude=data['user_log']['latitude'],
                        mac_address=data['user_log']['mac_address'],location=data['user_log']['location'])
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
                        return Response(util.success(self,{'user_info':{'id':user.id,'username':user.username,'usertypeobj':usertype.user_type,"agent_profile":agent_profile, "agentsubscription":agentsubscription, "add_on":add_on, "nb_sb":nb_sb, "billing":billing, "license_approve":license_approve, "is_social":user.is_social},'token':refresh,'msg':'login Success','profile':profileserializer.data,'image': serializer.data}))
                        
                    else:
                        return Response(util.success(self,{"popup":True})) 
                        
            else:                
                return Response(util.error(self,"Email not found"))  
        except Exception as e:
                return Response(util.error(self,str(e))) 


class ActivateDeactivate30Min(APIView):
    def put(self, request, format=None, slug=None):
        try:
            if slug is not None:
                userprofileobjid = UserProfile.objects.get(slug = slug)
                user,usertype, userprofile=get_user_usertype_userprofile(request, userprofileobjid.user_type.user.id)
                if userprofile:
                    obj_30min = min_30.objects.filter(userprofile = userprofile).last()
                    proppertyobj = Property_Detail.objects.filter(user_profile = userprofile)
                    if obj_30min.is_active == True:
                        obj_30min.is_active = False
                        for i in proppertyobj:
                            if i.min_30_shows == True:
                                i.min_30_shows = False
                                i.save()
                    else:
                        obj_30min.is_active = True
                        for i in proppertyobj:
                            if i.min_30_shows == False:
                                i.min_30_shows = True
                                i.save()
                    obj_30min.save()
                    return Response(util.success(self, "Successfully Updated Status"))
                else:
                    return Response(util.error(self, 'Invalid user'))
            else:
                return Response(util.error(self, 'Invalid id provided'))
        except Exception as e:
            return Response(util.error(self,str(e)))



class SalesPersonSearch(APIView):
    def post(self, request, format = None):
        try:
            data = request.data
            if data['search'] is not None:
                usertype_obj = UserType.objects.filter(user_type = 2)
                userprofile_obj = UserProfile.objects.filter(
                    Q(first_name__icontains=data['search']) |
                    Q(last_name__icontains=data['search']) |
                    Q(state__state_name__icontains=data['search']) |
                    Q(citymaster__city_name__icontains=data['search']) |
                    Q(areamaster__area_name__icontains=data['search']),
                    user_type__in = usertype_obj,
                )

                serializer = SalesPersonSearchSerializer(userprofile_obj, many=True)
                if serializer.data:
                    return Response(util.success(self, serializer.data))
                else:
                    return Response(util.success(self, 'Data not found'))
            else:
                return Response(util.error(self, 'search is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class SalesPersonSearch(APIView):
    def post(self, request, format = None):
        try:
            data = request.data
            if data['search'] is not None and data['user'] is not None:
                user, usertype, userprofile=get_user_usertype_userprofile(request, data['user'])
                usertype_obj = UserType.objects.filter(user_type = 2)
                userprofile_obj = UserProfile.objects.filter(
                    Q(first_name__icontains=data['search']) |
                    Q(last_name__icontains=data['search']) |
                    Q(state__state_name__icontains=data['search']) |
                    Q(citymaster__city_name__icontains=data['search']) |
                    Q(areamaster__area_name__icontains=data['search']),
                    user_type__in = usertype_obj,
                )
                paginator = MyPagination()
                paginated_queryset = paginator.paginate_queryset(userprofile_obj, request)
                serializer = SalesPersonSearchSerializer(paginated_queryset, context={'user':user}, many=True)
                if serializer.data:
                    return Response(util.success(self, serializer.data))
                else:
                    return Response(util.success(self, 'Data not found'))
            else:
                return Response(util.error(self, 'search is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class SalespersonSavedbyGuest(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
            if data['user_id'] is not None and data['sales_person_id'] is not None:
                user, usertype, userprofile=get_user_usertype_userprofile(request, data['user_id'])
                if user:
                    sales_user_id = UserProfile.objects.filter(id__in = data['sales_person_id'])
                    for i in sales_user_id:
                        user_profile_obj = UserProfile.objects.get(id=i.id)
                        sales_person_saved = SavedSalesPerosn.objects.create(user = user, userprofile = user_profile_obj)
                    return Response(util.success(self, "Saved Successfully"))
                else:
                    return Response(util.error(self, 'Invalid user'))
            else:
                return Response(util.error(self, 'user_id and sales_person_id are required'))
        except Exception as e:
            return Response(util.error(self,str(e)))
    
    def get(self, request, format = None, id = None):
        try:
            user, usertype, userprofile=get_user_usertype_userprofile(request, id)
            if user:
                sales_person_saved = SavedSalesPerosn.objects.filter(user = user).values_list('userprofile', flat=True)
                userprofile_obj = UserProfile.objects.filter(id__in = sales_person_saved)
                paginator = MyPagination()
                paginated_queryset = paginator.paginate_queryset(userprofile_obj, request)
                serializer = SalesPersonSearchSerializer(paginated_queryset, context={'user':user}, many=True)
                if serializer.data:
                    return Response(util.success(self, serializer.data))
                else:
                    return Response(util.success(self, 'Data not found'))
            else:
                return Response(util.error(self, 'Invalid user'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class DeleteSavedSalesPerson(APIView):
    def post(self, request, format = None):
        try:
            data = request.data
            if data['user_id'] is not None and data['sales_person_id'] is not None:
                user, usertype, userprofile=get_user_usertype_userprofile(request, data['user_id'])
                if user:
                    delete_saved_person = SavedSalesPerosn.objects.filter(user = user, userprofile__in = data['sales_person_id']).delete()
                    return Response(util.success(self, "Deleted Successfully"))
                else:
                    return Response(util.error(self, 'Invalid user'))
            else:
                return Response(util.error(self, 'user_id and sales_person_id are required'))
        except Exception as e:
                return Response(util.error(self,str(e)))

class LandloardProfileSetting(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def put(self, request, format= None):
        try:
            user_id = request.POST.get('user_id')
            profile_image=request.FILES.get('profile_image')
            business_name = request.POST.get('business_name')
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            cell_number=request.POST.get('cell_number')
            work_number=request.POST.get('work_number')
            home_address=request.POST.get('corp_address')
            town=request.POST.get('work_city_id')
            state_id=request.POST.get('work_state_id')
            zip_code=request.POST.get('work_zipcode')
            additional_seats = request.POST.get('additional_seats')
            number_of_seats = request.POST.get('no_of_seats')
            slug = request.POST.get('slug')
            if user_id != None:
                user,usertype,userprofile=get_user_usertype_userprofile(request,user_id)
                if userprofile:
                    if slug:
                        userprofile.slug = slug
                    if profile_image:
                        userprofile.profile_image=profile_image
                    if business_name:
                        userprofile.name_of_business_listing = business_name
                    if first_name:
                        userprofile.first_name=first_name
                    if last_name:
                        userprofile.last_name=last_name 
                    if  work_number:   
                        userprofile.work_number_1=work_number
                    if  cell_number:   
                        userprofile.cell_number=cell_number
                    if zip_code:
                        userprofile.zip_code=zip_code
                    if home_address:
                        userprofile.address_line_1=home_address
                    if additional_seats:
                        userprofile.addition_user=additional_seats
                    if number_of_seats:
                        userprofile.number_user=number_of_seats
                    if CityMaster.objects.filter(id=town):
                        userprofile.citymaster=CityMaster.objects.get(id=town)
                    if StateMaster.objects.filter(id=state_id):
                        userprofile.state=StateMaster.objects.get(id=state_id)
                    userprofile.save()
                    return Response(util.success(self,'Saved Successfully'))
                else:
                    return Response(util.error(self,'Profile Not Found'))
            else:
                return Response(util.error(self,'User Not Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))
    
    def get(self, request, format = None, slug=None):
        try:
            if slug is not None:
                userprofileobjid = UserProfile.objects.get(slug = slug)
                user,usertype, userprofile=get_user_usertype_userprofile(request, userprofileobjid.user_type.user.id)
            else:
                user,usertype, userprofile=get_user_usertype_userprofile(request, request.GET.get('id'))
            if user:
                if userprofile:
                    serializer=AgentProfileSerializer(userprofile)
                    return Response(util.success(self, serializer.data))
                else:
                    return Response(util.error(self,'User Id Not Match'))
            else:  
                return Response(util.error(self,'User not found'))
        except Exception as e:
            return Response(util.error(self,str(e)))
