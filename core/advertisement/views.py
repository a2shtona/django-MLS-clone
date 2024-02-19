from django.shortcuts import render, redirect
from accounts.models import User
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
from .models import *
from accounts.views import get_tokens_for_user,get_user_usertype_userprofile
from django.utils.decorators import method_decorator

from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils import timezone
from master import util
from .serializer import *
import datetime
import uuid
from django.core.mail import send_mail
# from master.utils import Util
from accounts.utils import Util
from accounts.profilepasswordviews import encrypt, decrypt, key
# Create your views here.
import jwt




# class AdvertismentUserView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, format=None):
#         data=request.data
#         if  "first_name" in data and "last_name" in data and "email" in data and  "password" in data:
#             if AdvertismentUser.objects.filter(email=data["email"]):
#                 return Response(util.success(self,'User is already registered'))
#             else:    
#                 date_joined = datetime.date.today()
#                 encrypted_string = encrypt(key, data['password'])
#                 advertismentuserid=uuid.uuid4()
#                 advertismentusershort= advertismentuserid.clock_seq_low
#                 advertismentuseridfinal=hex(int(advertismentusershort))[1:]
#                 advertisement=AdvertismentUser.objects.create(first_name=data["first_name"], last_name=data["last_name"], email=data["email"],password=encrypted_string ,date_joined=date_joined,AdvertismentUser_id=advertismentuseridfinal,) 
#                 advertisement.last_login=datetime.date.today()
#                 advertisement.is_active=True
#                 advertisement.save()
#                 return Response(util.success(self,'Registration successful'))
#         else:
#             return Response(util.error(self,'first_name, last_name, email, password is needed'))

key = '01234567890123456789015545678901'

class AdvertismentUserView(APIView):
    def post(self, request, format= None):
        try:
            data = request.data
            if 'Business_Name' in data and 'Business_Email' in data and 'Business_Phone' in data and 'password' in data and 'Industry' in data:
                if AdvertismentUser.objects.filter(Business_Email = data['Business_Email']):
                    return Response(util.success(self,'User is already registered'))
                else:
                    date_joined = datetime.date.today()
                    encrypted_string = encrypt(key, data['password'])
                    advertismentuserid=uuid.uuid4()
                    advertismentusershort= advertismentuserid.clock_seq_low
                    advertismentuseridfinal=hex(int(advertismentusershort))[1:]
                    advertisement = AdvertismentUser.objects.create(
                        Business_Name = data['Business_Name'],Business_Phone=data['Business_Phone'],
                        Business_Email = data['Business_Email'], password=encrypted_string ,date_joined=date_joined,
                        AdvertismentUser_id=advertismentuseridfinal, Industry=data['Industry']
                    )
                    advertisement.last_login=datetime.date.today()
                    advertisement.is_active=True
                    advertisement.save()
                    return Response(util.success(self,'Registration successful'))
            else:
                return Response(util.error(self,'Business_Name, Business_Email, Business_Phone, password, Industry is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

                

class AdvertismentLogin(APIView):
    def post(self, request, format=None):
        try:
            data=request.data
            # print(data)
            if "email" in data and "password" in data:
                if AdvertismentUser.objects.filter(Business_Email=data["email"]):
                    advertiseobj=AdvertismentUser.objects.get(Business_Email=data["email"])
                    decrypted_password = decrypt(key, advertiseobj.password)
                    if decrypted_password == data['password']:
                        # SECRET_KEY = 'secret'
                        token=jwt.encode({data['email']:data['password']}, "SECRET_KEY", algorithm="HS256")
                        # print(token)
                        serializer=AdvertismentRegistrationSerializer(advertiseobj)
                        # print(serializer.data)
                        return Response(util.success(self,{'user_info':serializer.data,'token':token,'msg':'login Success'}))
                    else:
                        return Response(util.error(self, 'password not match'))
                else:
                    return Response(util.error(self, 'Email not match'))
            else:
                return Response(util.error(self,'email, password is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))



class AdvertismentSave(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            data=request.data
            if  'AdvertismentUser_id' in data and 'Image' in data and 'description' in data and 'date' in data and 'advertisment_start_date' in data and 'advertisment_end_date' in data and 'title' in data:
                if AdvertismentUser.objects.filter(id=data['AdvertismentUser_id']):
                    advertismentuserobj=AdvertismentUser.objects.get(id=data['AdvertismentUser_id'])
                    # print(advertismentuserobj)
                    Image=request.FILES.get('Image')
                    description=request.POST.get('description')
                    date=request.POST.get('date')
                    advertisment_start_date=request.POST.get('advertisment_start_date')
                    advertisment_end_date=request.POST.get('advertisment_end_date')
                    title=request.POST.get('title')
                    is_approved_date=request.POST.get('is_approved_date')
                    obj=Advertisement.objects.create(AdvertismentUser_id=advertismentuserobj,Image=Image,description=description, advertisment_start_date=advertisment_start_date, advertisment_end_date=advertisment_end_date, title=title,is_approved_date=is_approved_date,date=date)
                    # print(obj)
                    return Response(util.success(self, 'Advertisement Created successfully'))
            else:
                return Response(util.error(self, 'AdvertismentUser_id not found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

    def get(self, request, format=None, id=None):
        try:
            if id is not None:
                if Advertisement.objects.filter(AdvertismentUser_id=id):
                    advertismentobj=Advertisement.objects.filter(AdvertismentUser_id=id)
                    # print(advertismentobj)
                    serializer=AdvertismentSerializer(advertismentobj, many=True)
                    # print(serializer.data)
                    if serializer.data:
                        return Response(util.success(self,serializer.data))
                    else:
                        return Response(util.error(self,"No Data Found"))
                
                else:
                    return Response(util.error(self, 'Advertisement id not found'))
            else:
                return Response(util.error(self, 'id is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))        

