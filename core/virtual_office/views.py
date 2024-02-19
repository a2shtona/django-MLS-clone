import email
from requests import delete
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.core import serializers as core_serializers
from django.views.decorators.csrf import csrf_exempt
from .serializer import *
from  .models import *
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.db.models import Avg
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework.parsers import MultiPartParser, FormParser

from accounts.paginatorviews import MyPagination
from .models import *
from accounts.views import get_user_usertype_userprofile
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
from accounts.views import get_tokens_for_user
from geopy.geocoders import Nominatim
import datetime
from django.db.models import Q

class CreateVirtualOffice(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, fromat=None):
        try:
            data = request.data
            if "userid" in data and "Virtual_Office_Name" in data and "Invite_Member" in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['userid'])
                if userprofile:
                    if VirtualOffice.objects.filter(virtual_office_name = data['Virtual_Office_Name']):
                        return Response(util.error(self, 'Office name is already in use'))
                    else:
                        virtualobj = VirtualOffice.objects.create(userprofile = userprofile, virtual_office_name = data['Virtual_Office_Name'])
                        first_email = data['Invite_Member'][0]
                        for i in data['Invite_Member']:
                            expirytime = datetime.datetime.now() + datetime.timedelta(hours=3)
                            if User.objects.filter(email = i):
                                virtualteamobj=VirtualOfficeTeam.objects.create(
                                    virtualid = virtualobj, email = i, expiration_date = expirytime, is_status = True
                                )
                                userobj = User.objects.get(email = i)
                                usertypeobj = UserType.objects.get(user = userobj)
                                userprofileid = UserProfile.objects.get(user_type = usertypeobj)
                                if userprofileid.first_name is None and userprofileid.last_name is None:
                                    contact_now = customer_info.objects.create(
                                        user = virtualteamobj, email = i, contact_no_1 = userprofile.cell_number, current_address = userprofile.address_line_1, origin_email = i
                                    )
                                else:
                                    contact_now = customer_info.objects.create(
                                        user = virtualteamobj, email = i, name = userprofileid.first_name+' '+userprofileid.last_name, contact_no_1 = userprofile.cell_number, current_address = userprofile.address_line_1, origin_email = i
                                    )
                                absurl = settings.SITE_URL+'login'
                            else:
                                virtualteamobj=VirtualOfficeTeam.objects.create(
                                    virtualid = virtualobj, email = i, expiration_date = expirytime, is_status = False
                                )
                                contact_now = customer_info.objects.create(
                                    email = i,user = virtualteamobj, origin_email = i)
                                absurl = settings.SITE_URL+'signup'
                            if first_email == i:
                                virtualteamobj.member_type = "Main"
                            else:
                                virtualteamobj.member_type = "Other"
                            
                            virtualteamobj.save()

                            uid = urlsafe_base64_encode(force_bytes(virtualteamobj.id))
                            send_mail(
                                'Invitation to join our site',
                                'Click the link to accept the invitation:'+absurl+'?uid='+uid+'&'+'token='+str(virtualteamobj.token),
                                'invitations@example.com',
                                [virtualteamobj.email],
                                fail_silently=False,
                            )
                        return Response(util.success(self, 'Email Send'))
                else:
                    return Response(util.error(self, 'UserProfile is not valid'))
            else:
                return Response(util.error(self, 'userid, Virtual_Office_Name, Invite_Member is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))
    
    def get(self, request, fromat=None, id=None):
        try:
            if id is not None:
                user,usertype,userprofile=get_user_usertype_userprofile(request, id)
                if userprofile:
                    virtualobj = VirtualOffice.objects.filter(userprofile = userprofile).order_by('-pk')
                    serializer = VisualProfileTeamSerializer(virtualobj,many=True)
                    if serializer.data:
                        return Response(util.success(self, serializer.data))
                    else:
                        return Response(util.error(self,"data not found"))
                else:
                    return Response(util.error(self, 'User is not valid'))
            else:
                return Response(util.error(self,"id is required"))
        except Exception as e:
            return Response(util.error(self,str(e)))
    
    def delete(self, request, fromat = None, id = None):
        try:
            if id is not None:
                virtualobj = VirtualOffice.objects.filter(id = id)
                virtualobj.delete()
                return Response(util.success(self, 'Delete was successful'))
            else:
                return Response(util.error(self,"id is required"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class VirtulaOfficenameShow(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request, format=None, id = None):
        try:
            if id is not None:
                user,usertype,userprofile=get_user_usertype_userprofile(request, id)
                if userprofile:
                    virtualobj = VirtualOffice.objects.filter(userprofile = userprofile.id)
                    serializer = VirtualOfficeNameSerializer(virtualobj, many=True)
                    if serializer.data:
                        return Response(util.success(self, serializer.data))
                    else:
                        return Response(util.error(self,"data not found"))
                else:
                    return Response(util.error(self, 'User is not valid'))
            else:
                return Response(util.error(self,"id is required"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class VirtualOfficePropertySend(APIView):
    def post(self, request, format= None):
        try:
            data = request.data
            if data['user_id'] is not None and data['virtual_id'] is not None and data['propertyid'] is not None:
                user,usertype,userprofile=get_user_usertype_userprofile(request, data['user_id'])
                if user:
                    virtualobj = VirtualOffice.objects.get(id = data['virtual_id'])
                    propertyobj = Property_Detail.objects.filter(id__in = data['propertyid'])
                    note = data['note']
                    user_id = data['user_id']
                    userobj = User.objects.get(id=user_id)
                    for i in propertyobj:
                        propertyid = Property_Detail.objects.get(id = i.id)
                        if not VirtualOfficeProperty.objects.filter(propertyid=propertyid,virtualofficeid=virtualobj,user=userobj):
                            VirtualOfficeProperty.objects.create(
                                userprofile = userprofile,virtualofficeid = virtualobj, propertyid = propertyid, note = note, user=userobj
                            )
                        else:
                            virtualpropertyobj = VirtualOfficeProperty.objects.get(Q(propertyid=propertyid),Q(virtualofficeid=virtualobj),Q(user=user_id))
                            virtualpropertyobj.note = note
                            virtualpropertyobj.save()
                    return Response(util.success(self, 'Successfully Send'))
                else:
                    return Response(util.error(self, 'Invalid user'))
            else:
                return Response(util.error(self,"user_id and propertyid is required"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class NotePropertyVirtualOfiice(APIView):
    def post(self, request, format = None):
        try:
            data = request.data
            if data['user_id'] is not None and data['propertyid'] is not None and data['note'] is not None and data['virtual_ofice'] is not None:
                user,usertype,userprofile=get_user_usertype_userprofile(request, data['user_id'])
                if user:
                    virtual_office = VirtualOffice.objects.get(id = data['virtual_ofice'])
                    propertyobj = Property_Detail.objects.get(id = data['propertyid'])
                    user_id = data['user_id']
                    userobj = User.objects.get(id=user_id)
                    if VirtualOfficeProperty.objects.filter(virtualofficeid = virtual_office, propertyid = propertyobj, user=user):
                        noteobj = VirtualOfficeProperty.objects.filter(propertyid = propertyobj,user=user).get(virtualofficeid = virtual_office)
                        noteobj.note = data['note']
                        noteobj.save()
                    else:
                        VirtualOfficeProperty.objects.create(propertyid = propertyobj, virtualofficeid = virtual_office, note = data['note'], user = userobj)

                    return Response(util.success(self, 'Successfully Added Note'))
                else:
                    return Response(util.error(self, 'Invalid user'))
            else:
                return Response(util.error(self,'user_id, propertyid, note is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class PropertyInterestinAPI(APIView):
    def post(self, request, fromat = None):
        try:
            data = request.data
            if data['user_id'] is not None and data['propertyid'] is not None and data['like'] is not None and data['virtual_ofice'] is not None:
                user,usertype,userprofile=get_user_usertype_userprofile(request, data['user_id'])
                if user:
                    virtual_office = VirtualOffice.objects.get(id = data['virtual_ofice'])
                    propertyobj = Property_Detail.objects.get(id = data['propertyid'])
                    if VirtualOfficeProperty.objects.filter(virtualofficeid = virtual_office, propertyid = propertyobj,user=user):
                        likeobj = VirtualOfficeProperty.objects.filter(propertyid = propertyobj,user=user).get(virtualofficeid = virtual_office)
                        likeobj.is_like = True
                        likeobj.is_dislike = False
                        likeobj.user = user
                        likeobj.userprofile = userprofile
                        likeobj.save()
                    else:
                        likeobj = VirtualOfficeProperty.objects.create(virtualofficeid = virtual_office, propertyid = propertyobj,is_like = True,is_dislike = False,user = user,userprofile = userprofile)
                    return Response(util.success(self, "Liked Property"))
                else:
                    return Response(util.error(self, 'Invalid user'))
            else:
                return Response(util.error(self,'user_id, propertyid, like is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))
    
    def get(self, request, fromat= None, id= None):
        try:
            if id is not None:
                noteobj = VirtualOfficeProperty.objects.filter(virtualofficeid = id,user=request.user).filter(is_like = True)
                serializer = VirtualOffice_Like_Dislike_Note_Serializer(noteobj, many=True)
                if serializer.data:
                    return Response(util.success(self, serializer.data))
                else:
                    return Response(util.error(self,"data not found"))
            else:
                return Response(util.error(self, 'id is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class PropertyDislikeinAPI(APIView):
    def post(self, request, format = None):
        try:
            data = request.data
            if data['user_id'] is not None and data['propertyid'] is not None and data['dislike'] is not None and data['virtual_ofice'] is not None:
                user,usertype,userprofile=get_user_usertype_userprofile(request, data['user_id'])
                if user:
                    virtual_office = VirtualOffice.objects.get(id = data['virtual_ofice'])
                    propertyobj = Property_Detail.objects.get(id = data['propertyid'])
                    if VirtualOfficeProperty.objects.filter(virtualofficeid = virtual_office, propertyid = propertyobj,user=user):
                        likeobj = VirtualOfficeProperty.objects.filter(propertyid = propertyobj,user=user).get(virtualofficeid = virtual_office)
                        likeobj.is_like = False
                        likeobj.is_dislike = True
                        likeobj.user = user
                        likeobj.userprofile = userprofile
                        likeobj.save()
                    else:
                        likeobj = VirtualOfficeProperty.objects.create(virtualofficeid = virtual_office, propertyid = propertyobj, is_like = False, is_dislike = True, user = user,userprofile = userprofile)
                    return Response(util.success(self, "Liked Property"))
                else:
                    return Response(util.error(self, 'Invalid user'))
            else:
                return Response(util.error(self,'user_id, propertyid, like is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))
    
    def get(self, request, fromat= None, id= None):
        try:
            if id is not None:
                noteobj = VirtualOfficeProperty.objects.filter(virtualofficeid = id,user=request.user).filter(is_dislike = True)
                serializer = VirtualOffice_Like_Dislike_Note_Serializer(noteobj, many=True)
                if serializer.data:
                    return Response(util.success(self, serializer.data))
                else:
                    return Response(util.error(self,"data not found"))
            else:
                return Response(util.error(self, 'id is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class DeleteVirtualOfficeProperty(APIView):
    def get(self, request, format=None, id= None):
        try:
            if id is not None:
                note = VirtualOfficeProperty.objects.get(id=id)
                note.delete()
                return Response(util.success(self, 'Delete Successfully'))
            else:
                return Response(util.error(self, 'id is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class ShowAgentProfileOnVirtualOffice(APIView):
    def get(self, request, format=None, id=None):
        try:
            if id is not None:
                user,usertype,userprofile=get_user_usertype_userprofile(request, id)
                if user:
                    userobj = VirtualOfficeTeam.objects.filter(email = user.email).values_list('virtualid', flat=True)
                    officeobj = VirtualOffice.objects.filter(id__in = userobj)
                    serializer = AgentProfileVirtualOfficeSerializer(officeobj, many=True)
                    if serializer.data:
                        return Response(util.success(self, serializer.data))
                    else:
                        return Response(util.error(self,"data not found"))
                else:
                    return Response(util.error(self, 'User is not valid'))
            else:
                return Response(util.error(self, 'id is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class ExitVirtualOffice(APIView):
    def post(self, request, format= None):
        try:
            data = request.data
            if data['user_id'] is not None and data['virtual_id'] is not None:
                user,usertype,userprofile=get_user_usertype_userprofile(request, data['user_id'])
                if user:
                    officeobj = VirtualOffice.objects.get(id = data['virtual_id'])
                    userobj = VirtualOfficeTeam.objects.filter(email = user.email).get(virtualid = officeobj).delete()
                    return Response(util.success(self, 'Exit Successfully'))
                else:
                    return Response(util.error(self, 'User is not valid'))
            else:
                return Response(util.error(self,'user_id, virtual_id is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))
        
class GetVirtualTeamlist(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None, id = None):
        try:
            if id is not None:
                virtualteam = VirtualOfficeTeam.objects.filter(virtualid = id)
                serializer = VirtualOfficeTeamId(virtualteam, many= True)
                if serializer.data:
                    return Response(util.success(self, serializer.data))
                else:
                    return Response(util.error(self,"data not found"))
            else:
                return Response(util.error(self, "Id is required"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class VirtualOfficeTeamProfile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None, id=None):
        try:
            if id is not None:
                customobj = customer_info.objects.get(id = id)
                serailizer = Custom_Info_Image_Serializer(customobj)
                if serailizer.data:
                    return Response(util.success(self, serailizer.data))
                else:
                    return Response(util.error(self, 'Data not Found'))
            else:
                return Response(util.error(self, 'Invalid id provided'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class EditCustomUser(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, format=None, id=None):
        try:
            user, usertype, userprofile = get_user_usertype_userprofile(request, request.user.id)
            if id is not None:
                if customer_info.objects.get(id = id):
                    customobj = customer_info.objects.get(id = id)
                    data = request.POST
                    if data['name'] is not None:
                        customobj.name = data['name']
                    if data['dob'] is not None:
                        customobj.dob = datetime.datetime.strptime(data['dob'], '%Y-%m-%d').date()
                    if data['contact_no_1'] is not None:
                        customobj.contact_no_1 = data['contact_no_1']
                    if data['contact_no_2'] is not None:
                        customobj.contact_no_2 = data['contact_no_2']
                    if data['email'] is not None:
                        customobj.email  = data['email']
                    if data['date_of_close'] is not None:
                        customobj.date_of_close = datetime.datetime.strptime(data['date_of_close'], '%Y-%m-%d').date()
                    if data['towns_of_interest'] is not None:
                        customobj.towns_of_interest = data['towns_of_interest']
                    if data['purchase_rental_price'] is not None:
                        customobj.purchase_rental_price = data['purchase_rental_price']
                    if data['current_address'] is not None:
                        customobj.current_address = data['current_address']
                    if data['add_note'] is not None:
                        customobj.add_note = data['add_note']
                    if data['martial_status'] is not None:
                        customobj.martial_status = data['martial_status']
                    if data['relationship'] is not None:
                        customobj.relationship = data['relationship']
                    customobj.is_edit = True
                    customobj.save()
                    signed_documents = request.FILES.getlist('signed_documents')
                    for i in signed_documents:
                        filename = i.name
                        Document.objects.create(
                            user = user, file = i, filename = filename, is_signed = True
                        )
                    return Response(util.success(self, 'Updated Successfully'))
                else:
                    return Response(util.error(self, 'Invalid Data'))
            else:
                return Response(util.error(self, 'Invalid id provided'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class PropertyUserShowVirtualOffice(APIView):
    def get(self, request, format=None, id=None):
        try:
            if id is not None:
                virtual_office = request.GET.get('Virtual_id')
                user,usertype,userprofile=get_user_usertype_userprofile(request, id)
                if userprofile:
                   virtuaofficeid = VirtualOffice.objects.get(id = virtual_office)
                   brokerobj = virtuaofficeid.userprofile
                   brokeremail = brokerobj.user_type.user
                   propertyobj = Property_Detail.objects.filter(user_profile = brokerobj, is_property_expired = False, is_property_open = True)
                   serializer = PropertyDetailvirtualSerializer(propertyobj, context={'virtual_id':virtuaofficeid,"userid":request.user}, many=True)
                   if serializer.data:
                        return Response(util.success(self, serializer.data))
                   else:
                        return Response(util.error(self, "Data Not Found"))
                else:
                    return Response(util.error(self, 'Invalid user'))
            else:
                return Response(util.error(self, 'id required'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class VitualOfficeUserName(APIView):
    def get(self, request, format=None, id = None):
        try:
            if id is not None:
                user,usertype,userprofile=get_user_usertype_userprofile(request, id)
                if user:
                    virtualteam = VirtualOfficeTeam.objects.filter(email = user.email).values_list('virtualid',flat=True)
                    virtualobj = VirtualOffice.objects.filter(id__in = virtualteam)
                    serializer = VirtualOfficeNameSerializer(virtualobj, many=True)
                    if serializer.data:
                        return Response(util.success(self, serializer.data))
                    else:
                        return Response(util.error(self,"data not found"))
                else:
                    return Response(util.error(self, 'User is not valid'))
            else:
                return Response(util.error(self,"id is required"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class AgentReviewGuestProfile(APIView):
    def get(self, request, fromat=None, id=None):
        try:
            if id is not None:
                user,usertype,userprofile=get_user_usertype_userprofile(request, id)
                if userprofile:
                    virtualobj = VirtualOffice.objects.filter(userprofile = userprofile.id).values_list('id', flat=True)
                    officeteam = VirtualOfficeTeam.objects.filter(virtualid__in = virtualobj, is_status = True)
                    user_id = []
                    for i in officeteam:
                        if User.objects.filter(email = i.email):
                            user = User.objects.get(email = i.email)
                            user_id.append(user)
                        else:
                            pass
                    
                    usertype_obj = UserType.objects.filter(user__in = user_id)
                    userprofile_obj = UserProfile.objects.filter(user_type__in = usertype_obj)

                    serializer = ReviewUserProfileSerializer(userprofile_obj, many=True)
                    if serializer.data:
                        return Response(util.success(self, serializer.data))
                    else:
                        return Response(util.error(self, 'No data Found'))
                else:
                    return Response(util.error(self, 'User is not valid'))
            else:
                return Response(util.error(self,"id is required"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class GuestReviewAgentProfile(APIView):
    def get(self, request, fromat=None, id=None):
        try:
            if id is not None:
                user,usertype,userprofile=get_user_usertype_userprofile(request, id)
                if user:
                    userobj = VirtualOfficeTeam.objects.filter(email = user.email).values_list('virtualid', flat=True)
                    officeobj = VirtualOffice.objects.filter(id__in = userobj).values_list('userprofile', flat=True)
                    userprofile_obj = UserProfile.objects.filter(id__in = officeobj)

                    serializer = ReviewUserProfileSerializer(userprofile_obj, many=True)
                    if serializer.data:
                        return Response(util.success(self, serializer.data))
                    else:
                        return Response(util.error(self, 'No data Found'))
                else:
                    return Response(util.error(self, 'User is not valid'))
            else:
                return Response(util.error(self,"id is required"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class AgnetUnExpiredListingProperty(APIView):
    def post(self, request, format=None):
        try:
            if request.data['user_id'] is not None and request.data['date'] is not None:
                user,usertype,userprofile=get_user_usertype_userprofile(request,request.data['user_id'])
                if usertype.user_type==2 or usertype.user_type==4 or usertype.user_type==5:
                    if userprofile:
                        today = datetime.datetime.strptime(request.data['date'], "%Y-%m-%d")
                        if Property_Detail.objects.filter(user_profile=userprofile.id):
                            propertyobj=Property_Detail.objects.filter(user_profile=userprofile, is_property_expired=False, is_property_open=True).values_list('id', flat=True)
                            teamproperty = TeamProperty.objects.filter(userprofile_id=userprofile)
                            propertyevnetobj = Property_listing_event.objects.filter(property_details__in = propertyobj)
                            for i in propertyevnetobj:
                                end_date = i.property_listing_end_date
                                if end_date is not None:
                                    if end_date.date() <= today.date():
                                        propertyid = Property_Detail.objects.get(id = i.property_details.id)
                                        propertyid.is_property_expired = True
                                        propertyid.save()
                            
                            propertyidobj=Property_Detail.objects.filter(user_profile=userprofile, is_property_expired=False, is_property_open=True)

                            serializer=PropertyDetailvirtualSerializer(propertyidobj, context={'userid':user.id}, many=True)
                            serializer1=AgnetTeamPropertySerializer(teamproperty, context={'userid':user.id}, many = True)
                            
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
                return Response(util.error(self,'user_id, date are required'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class GuestAgentProfileView(APIView):
    def get(self, request, id= None):
        try:
            if id is not None:
                if VirtualOffice.objects.filter(id = id):
                    agentprofile = VirtualOffice.objects.get(id = id)
                    serializer = GuestAgentProfileViewSerializer(agentprofile)
                    if serializer.data:
                        return Response(util.success(self, serializer.data))
                    else:
                        return Response(util.error(self, 'Data not Found'))
                else:
                    return Response(util.error(self, 'Error 404'))
            else:
                return Response(util.error(self,'id is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class GetTeamProfile(APIView):
    def get(self, request, id = None):
        try:
            if id is not None:
                user,usertype,userprofile=get_user_usertype_userprofile(request,id)
                if userprofile:
                    vitualobj = VirtualOffice.objects.filter(userprofile = userprofile).values_list('id', flat=True)
                    virtualteam = VirtualOfficeTeam.objects.filter(virtualid__in = vitualobj, is_status = True).values_list('email', flat=True).distinct()
                    # print(virtualteam)
                    serializer = VitualOfficeTeamSerializer(virtualteam, many=True)
                    if serializer.data:
                        return Response(util.success(self, serializer.data))
                    else:
                        return Response(util.error(self,"data not found"))
                else:
                    return Response(util.error(self, 'User not found'))
            else:
                return Response(util.error(self,'id is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class SearchTeamPerson(APIView):
    def post(self, request, format = None):
        try:
            data = request.data
            if data['search'] is not None and data['user'] is not None:
                user, usertype, userprofile=get_user_usertype_userprofile(request, data['user'])
                vitualobj = VirtualOffice.objects.filter(userprofile = userprofile)
                usertype_obj = UserType.objects.filter(user_type = 1)
                user_profile_obj = UserProfile.objects.filter(
                    Q(first_name__icontains=data['search']) |
                    Q(last_name__icontains=data['search']) ,
                    user_type__in = usertype_obj
                ).values_list('user_type', flat=True)
                usertype_id = UserType.objects.filter(id__in = user_profile_obj).values_list('user', flat=True)
                user_id = User.objects.filter(id__in = usertype_id).values_list('email', flat=True)

                virtualteam = VirtualOfficeTeam.objects.filter(virtualid__in = vitualobj, email__in = user_id, is_status = True).values_list('email', flat=True).distinct()
                
                serializer = VitualOfficeTeamSerializer(virtualteam, many= True)
                if serializer.data:
                    return Response(util.success(self, serializer.data))
                else:
                    return Response(util.error(self,"data not found"))
            else:
                return Response(util.error(self,'search and user is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))
