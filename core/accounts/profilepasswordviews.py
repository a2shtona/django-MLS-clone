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
# from Crypto.Cipher import AES
import base64
from .views import get_tokens_for_user
import hashlib
from Cryptodome.Cipher import AES
import os
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

key = '01234567890123456789015545678901'

def encrypt(key, plaintext):
    # Convert the key and plaintext to bytes
    key = key.encode('utf-8')
    plaintext = plaintext.encode('utf-8')
    # Generate a random initialization vector
    iv = os.urandom(16)
    # Create a new Cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Pad the plaintext to a multiple of 16 bytes
    padding_length = 16 - (len(plaintext) % 16)
    plaintext += bytes([padding_length]) * padding_length
    # Encrypt the plaintext and return the ciphertext and initialization vector
    ciphertext = cipher.encrypt(plaintext)
    return base64.b64encode(iv + ciphertext).decode('utf-8')

def decrypt(key, ciphertext):
    # Convert the key and ciphertext to bytes
    key = key.encode('utf-8')
    ciphertext = base64.b64decode(ciphertext.encode('utf-8'))
    # Extract the initialization vector
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    # Create a new Cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Decrypt the ciphertext and remove the padding
    plaintext = cipher.decrypt(ciphertext)
    padding_length = plaintext[-1]
    return plaintext[:-padding_length].decode('utf-8')

class Profile_Password(APIView):
    def post(self, request, format=None):
        try:
            data=request.data
            if 'Create_Admin_Password' in data and 'user_id' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['user_id'])
                if userprofile:
                    if data['Create_Admin_Password'] == True:
                        if 'profile_password' in data:
                            encrypted_string = encrypt(key, data['profile_password'])
                            userprofile.profile_password=encrypted_string
                            userprofile.is_profilepassword=True
                            userprofile.save()
                            return Response(util.success(self, 'Userprofile is Updated'))
                        else:
                            return Response(util.error(self, 'profile_password is needed'))
                    else:
                        return Response(util.error(self, 'skip this request'))
                else:
                    return Response(util.error(self, 'userprofile is not found'))
            else:
                return Response(util.error(self,'user_id is needed'))
        except Exception as e:
            return Response(util.error(self,str(e))) 

class CheckUserProfilePassword(APIView):
    def post(self, request, format = None):
        try:
            data = request.data
            if 'profile_password' in data and 'user_id' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['user_id'])
                if userprofile:
                    decrypted_password = decrypt(key, userprofile.profile_password)
                    # print(decrypted_password)
                    if decrypted_password == data['profile_password']:
                        token = get_tokens_for_user(user)
                        return Response(util.success(self, [{'userprofile_id':userprofile.id,'is_profilepassword':True}, token]))
                    else:
                        return Response(util.error(self, 'Password is incorrect'))
                else:
                    return Response(util.error(self, 'userprofile is not found'))
            else:
                return Response(util.error(self,'user_id, profile_password is required'))
        except Exception as e:
            return Response(util.error(self,str(e))) 

class Checkprofilepassword(APIView):
    def post(self, request, fromat= None):
        try:
            data = request.data
            if 'user_id' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['user_id'])
                if userprofile:
                    if userprofile.is_profilepassword == True:
                        token = get_tokens_for_user(user)
                        return Response(util.success(self, [{'is_profilepassword':True}, token]))
                    else:
                        return Response(util.error(self, {'is_profilepassword': False}))
                else:
                    return Response(util.error(self, 'userprofile is not found'))
            else:
                return Response(util.error(self,'user_id is needed'))
        except Exception as e:
            return Response(util.error(self,str(e))) 

class RemovePropefilePassword(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
            if 'user_id' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['user_id'])
                if userprofile:
                    decrypted_password = decrypt(key, userprofile.profile_password)
                    if decrypted_password == data['profile_password']:
                        userprofile.is_profilepassword = False
                        userprofile.profile_password = None
                        userprofile.save()
                        return Response(util.success(self, 'Successfully Updated'))
                    else:
                        return Response(util.error(self, 'Password is incorrect'))
                else:
                    return Response(util.error(self, "userprofile not found"))
            else:
                return Response(util.error(self, 'user_id is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class ForgetProfilePassword(APIView):
    def post(self, request, format = None):
        try:
            email = request.data.get("email")
            if email is not None:
                if User.objects.filter(email=email).exists():
                    user = User.objects.get(email=email)
                    usertype = UserType.objects.get(user=user)
                    userprofile = UserProfile.objects.get(user_type=usertype)
                    if userprofile.is_profilepassword == True:
                        uid = urlsafe_base64_encode(force_bytes(user.id))
                        token = PasswordResetTokenGenerator().make_token(user)
                        absurl = settings.SITE_URL+'agent-dashboard/profile-settings/reset-password/'+"?uid="+uid+'&'+"token="+token
                        email_body = 'Hi '+user.email + \
                        ' Use the link below to reset your password \n' + absurl
                        data = {'email_body': email_body, 'to_email': user.email,'email_subject': 'Verify your email'}
                        Util.send_email(data)
                        return Response(util.success(self,'Email Sent Successfull'))
                    else:
                        return Response(util.error(self, 'Please Create Admin Password'))
                else:
                    return Response(util.error(self,'User Not Found'))
            else:
                return Response(util.error(self, "email is required"))
        except Exception as e:
            return Response(util.error(self,str(e))) 

class ResetProfilePassword(APIView):
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
                usertype = UserType.objects.get(user=user)
                userprofile = UserProfile.objects.get(user_type=usertype)
                encrypted_string = encrypt(key, password)
                userprofile.profile_password = encrypted_string
                userprofile.save()
                return Response(util.success(self,'Password Updated Successfully'))
            else:
                return Response(util.error(self,'password and password1 is required'))
        except Exception as e:
            return Response(util.error(self,str(e))) 