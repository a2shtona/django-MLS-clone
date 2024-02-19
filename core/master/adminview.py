import calendar
from property.models import *
from .models import *
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.contrib.auth import authenticate,login ,logout
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.models import UserProfile

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from accounts.utils import Util
from accounts.models import *
from advertisment.models import *
from django.contrib import messages
from .resource import *
from tablib import Dataset
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

import secrets
from django.core.mail import EmailMessage
from boostmarketing.models import BoostMarketingServicesTOUser, BoostMarketingTable
from datetime import datetime, timedelta, date


from .views import get_user_usertype_userprofile

class AdminLogin(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('/AdminDashboard')
        return render(request, 'sign-in.html')
    
    def post(self,request):
        username= request.POST.get('username')
        password= request.POST.get('password')
        
        user=auth.authenticate(username=username,password=password)
        # print(user)
        if user is not None:
            if user.is_superuser:
                auth.login(request,user)
                return redirect('/AdminDashboard')
            else:
                return redirect('/')
        else:
            return redirect('/') 

import os
class Dashboard(View):
    @method_decorator(login_required(login_url='/'))
    def get(self,request):
        name=os.environ.get("DBNAME")
        return render(request,"index-2.html",{'name':name})
    
    def post(self,request):
        return redirect('/dashboard')

class UserList(View):
    @method_decorator(login_required(login_url='/'))
    def get(self,request):
        if 'q' in request.GET:
            q=request.GET['q']
            multiple_q=Q(Q(first_name__icontains=q)| Q(last_name__icontains=q)  | Q(cell_number__icontains=q))
            userprofile=UserProfile.objects.filter(multiple_q)
        else:
            userprofile=UserProfile.objects.all()

        # paginator
        paginator=Paginator(userprofile,20)
        page_number=request.GET.get('page')
        userprofile=paginator.get_page(page_number)
        obj=paginator.page_range
        context={ "obj":obj}
        return render(request,"user-list.html",context)

class GuestList(View):
    @method_decorator(login_required(login_url='/'))
    def get(self,request):
        guestlistid=UserType.objects.filter(user_type=1).values_list("id",flat=True)
        userprofile=UserProfile.objects.filter(user_type_id__in=guestlistid)
        # paginator
        paginator=Paginator(userprofile,20)
        page_number=request.GET.get('page')
        guestlistfinal=paginator.get_page(page_number)
        obj=paginator.page_range
        context={'userprofile':guestlistfinal, "obj":obj}
        return render(request,"user-list.html",context)

class AgentList(View):
    @method_decorator(login_required(login_url='/'))
    def get(self,request):
        agentlistid=UserType.objects.filter(user_type=2).values_list("id",flat=True)
        userprofile=UserProfile.objects.filter(user_type_id__in =agentlistid)
         # paginator
        paginator=Paginator(userprofile,20)
        page_number=request.GET.get('page')
        agentlistfinal=paginator.get_page(page_number)
        obj=paginator.page_range
        context={'userprofile':agentlistfinal, "obj":obj}
        return render(request,"user-list.html",context)

class InvestorDevloperlist(View):
    @method_decorator(login_required(login_url='/'))
    def get(self,request):
        InvestorDevloperlistid=UserType.objects.filter(user_type=3).values_list("id",flat=True)
        userprofile=UserProfile.objects.filter(user_type_id__in =InvestorDevloperlistid)
         # paginator
        paginator=Paginator(userprofile,20)
        page_number=request.GET.get('page')
        investerdevlopertlistfinal=paginator.get_page(page_number)
        obj=paginator.page_range
        context={'userprofile':investerdevlopertlistfinal, "obj":obj}
        return render(request,"user-list.html",context)

class FSBHOlist(View):
    @method_decorator(login_required(login_url='/'))
    def get(self,request):
        fsbholistid=UserType.objects.filter(user_type=4).values_list("id",flat=True)
        userprofile=UserProfile.objects.filter(user_type_id__in =fsbholistid)
        
         # paginator
        paginator=Paginator(userprofile,20)
        page_number=request.GET.get('page')
        FSBGOlistfinal=paginator.get_page(page_number)
        obj=paginator.page_range
        context={'userprofile':FSBGOlistfinal, "obj":obj}
        return render(request,"user-list.html",context)

class ManagementList(View):
    @method_decorator(login_required(login_url='/'))
    def get(self,request):
        managementlistid=UserType.objects.filter(user_type=4).values_list("id",flat=True)
        userprofile=UserProfile.objects.filter(user_type_id__in =managementlistid)
        # paginator
        paginator=Paginator(userprofile,20)
        page_number=request.GET.get('page')
        managementlistfinal=paginator.get_page(page_number)
        obj=paginator.page_range
        context={'userprofile':managementlistfinal, "obj":obj}
        return render(request,"user-list.html",context)

class SendVerifucationMail(View):
    def get(self,request):
        return render(request,"verify-account.html")
    
    def post(self,request):
        username = request.POST.get('username') 
        if User.objects.filter(username=username):
            user=User.objects.get(username=username)
            if user.is_superuser:
                token = RefreshToken.for_user(user).access_token
                current_site = get_current_site(request).domain
                relativeLink = reverse('email-verify')
                absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
                email_body = 'Hi '+user.username + \
                ' Use the link below to verify your email \n' + absurl
                data = {'email_body': email_body, 'to_email': user.username,'email_subject': 'Verify your email'}
                Util.send_email(data)
                messages.success(request, "Please Check Your Mail.")
                return redirect("/verify-email")

            else:
                messages.error(request, f"Not a Valid Admin User.")
                return redirect("/verify-email")
        else:
            messages.error(request, f"Admin User Not Found.")
            return redirect('/')
 
class LogoutView(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request):
        user = request.user
        # print(user)
        logout(request)
        return redirect('/')

class UserProfileView(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request,id):
        if UserProfile.objects.filter(id=id):
            userprofileobj=UserProfile.objects.get(id=id)
            
            if userprofileobj.user_type.user_type==1:
                propertyobj = Guest_Users_Save_Listing.objects.filter(user = userprofileobj.user_type.user.id) # Save Property
                propertyobj1 = Seen_Property_listing.objects.filter(user_profile_id = userprofileobj.user_type.user.id) # Seen Property
                propertyobj2 = None
                propertyobj3 = None
            elif userprofileobj.user_type.user_type==2:
                propertyobj = Property_Detail.objects.filter(user_profile = userprofileobj.id, is_property_open=True) # Open listing
                propertyobj1 = Property_Detail.objects.filter(user_profile = userprofileobj.id, is_property_open=False) # Close listing
                propertyobj2 = Property_Detail.objects.filter(user_profile = userprofileobj.id, is_property_expired=False) # current listing
                propertyobj3 = Property_Detail.objects.filter(user_profile = userprofileobj.id, is_property_expired=True) # expire listing
            else:
                propertyobj = None
                propertyobj1 = None
                propertyobj2 = None
                propertyobj3 = None
            context={"userprofileobj":userprofileobj,'propertyobj':propertyobj,'propertyobj1':propertyobj1,"propertyobj2":propertyobj2,"propertyobj3":propertyobj3}
            return render(request,"user-profile.html",context)
        elif User.objects.filter(id=id):
            user=User.objects.get(id=id)
            usertype=UserType.objects.get(user=user)
            userprofile=UserProfile.objects.get(user_type=usertype)
            propertyobj = None
            propertyobj1 = None
            propertyobj2 = None
            propertyobj3 = None
            context={"userprofileobj":userprofile,'propertyobj':propertyobj,'propertyobj1':propertyobj1,"propertyobj2":propertyobj2,"propertyobj3":propertyobj3}
            return render(request,"user-profile.html",context)
        else:
            messages.error(request, f"Proile Not Found")
            return redirect("/userlist")

class BlockUser(View):
    @method_decorator(login_required(login_url='/'))
    def post(self, request,pk):
        if request.user.is_superuser:
            if User.objects.filter(id=pk):
                userobj=User.objects.get(id=pk)
                userobj.is_active=False
                path=request.POST.get('path')
                userobj.save()
                return redirect(path)
            else:
                messages.error(request, f"Proile Not Found")
                return redirect("/userlist")
        else:
            messages.error(request, f"You are not a valid user to perfom this action.")
            return redirect("/userlist")

class UnBlockUser(View):
    @method_decorator(login_required(login_url='/'))
    def post(self, request,pk):
        if request.user.is_superuser:
            if User.objects.filter(id=pk):
                userobj=User.objects.get(id=pk)
                userobj.is_active=True
                path=request.POST.get('path')
                userobj.save()
                return redirect(path)
            else:
                messages.error(request, f"Proile Not Found")
                return redirect("/userlist")
        else:
            messages.error(request, f"You are not a valid user to perfom this action.")
            return redirect("/userlist")

class SuspendUser(View):
    @method_decorator(login_required(login_url='/'))
    def post(self, request,pk):
        if request.user.is_superuser:
            if User.objects.filter(id=pk):
                userobj=User.objects.get(id=pk)
                userobj.is_suspended=True
                path=request.POST.get('path')
                userobj.save()
                return redirect(path)
            else:
                messages.error(request, f"Proile Not Found")
                return redirect("/userlist")
        else:
            messages.error(request, f"You are not a valid user to perfom this action.")
            return redirect("/userlist")

class AddTypeOfListing(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request):
        if request.user.is_superuser:
            # search
            if 'q' in request.GET:
                q=request.GET['q']
                multiple_q=Q(Q(type_of_listing__icontains=q) | Q(listing_type__icontains=q))
                propertylistingtypeobj=Property_Listing_Type.objects.filter(multiple_q)
            else:    
                propertylistingtypeobj=Property_Listing_Type.objects.all()

            # paginator
            paginator=Paginator(propertylistingtypeobj,20)
            page_number=request.GET.get('page')
            propertylistingtypeobj=paginator.get_page(page_number)
            obj=paginator.page_range

            propety_listing_type=Propertylisting_type.objects.all()
            context={"propety_listing_type":propety_listing_type,"propertylistingtypeobj":propertylistingtypeobj, "obj":obj}
            return render(request, 'type-of-listing.html',context)

    def post(self, request,id=None):
        if request.user.is_superuser:
            action=request.POST.get('action')
            if action=="Delete":
                if id!=None and Property_Listing_Type.objects.filter(id=id):
                    listingtypeobj=Property_Listing_Type.objects.get(id=id)
                    listingtypeobj.delete()
                    return redirect('/typeoflisting')
                else:
                    return redirect('/typeoflisting')
            else:
                type_of_listing=request.POST.get('type_of_listing')
                propertytypelistingobj=Propertylisting_type.objects.get(id=type_of_listing)
                listing_type=request.POST.get('listing_type')
                user_listing_type = request.POST.get("user_listing_type")
                listingposition= request.POST.get('listingposition')
                Property_Listing_Type.objects.create(type_of_listing=propertytypelistingobj,listing_type=listing_type,listing_position=listingposition,user_listing_type=user_listing_type)
                return redirect('/typeoflisting')

        else:
            return redirect('/typeoflisting')

class UpdateTypeOfListing(View):
    @method_decorator(login_required(login_url='/'))
    def post(self, request,id):
        listing_type=request.POST.get('listing_type')
        listingposition= request.POST.get('listingposition')
        type_of_listing= request.POST.get('type_of_listing')
        # print(type_of_listing)
        if Propertylisting_type.objects.filter(property_listing_name = type_of_listing):
            propertyobj = Propertylisting_type.objects.get(property_listing_name = type_of_listing)
        else:
            propertyobj = None
        status= request.POST.get('status')
        if Property_Listing_Type.objects.filter(id=id):
            obj=Property_Listing_Type.objects.get(id=id)
            if propertyobj !=None:
                obj.type_of_listing=propertyobj
            if listingposition!=None:
                obj.listing_position=listingposition
            if listing_type!=None:
                obj.listing_type=listing_type
            if status!=None:
                if status == "False":
                    obj.is_active=False
                else:
                    obj.is_active=True
            
            obj.save()
        return redirect('/typeoflisting')

class PropertyMainCategory(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request):
        propertylistingtypeobj=Property_Listing_Type.objects.filter(is_active=True)
        # search
        if 'q' in request.GET:
            q= request.GET['q']
            multiple_q=Q(Q(Main_category__icontains=q))
            multiple_p=Q(Q(type_of_listing__icontains=q))

            propertylistingtypeobj=Property_Listing_Type.objects.filter(multiple_p).values_list('id', flat=True)
            propertymaincategoryobj_type=Property_Main_Category.objects.filter(listing_type__in=propertylistingtypeobj)
            propertymaincategoryobj_name=Property_Main_Category.objects.filter(multiple_q)
            propertymaincategoryobj=list(chain(propertymaincategoryobj_type, propertymaincategoryobj_name))
        else:
            propertymaincategoryobj=Property_Main_Category.objects.all()
        
        # paginator
        paginator=Paginator(propertymaincategoryobj,20)
        page_number=request.GET.get('page')
        propertymaincategoryobj=paginator.get_page(page_number)
        obj=paginator.page_range
        context={'propertylistingtypeobj':propertylistingtypeobj,'propertymaincategoryobj':propertymaincategoryobj,"obj":obj}
        return render(request,'Property_Main_Category.html',context)
    
    def post(self, request,id=None):
        if request.user.is_superuser:
            action=request.POST.get('action')
            if action=="Delete":
                if id!=None and Property_Main_Category.objects.filter(id=id):
                    maincategoryobj=Property_Main_Category.objects.get(id=id)
                    maincategoryobj.delete()
                    return redirect('/propertymaincategory')
                else:
                    return redirect('/propertymaincategory')
            else:
                propertytypelistinfid=request.POST.get('maincategoryid')
                listingtypeobj=Property_Listing_Type.objects.get(id=propertytypelistinfid)
                main_category_name=request.POST.get('main')
                listingposition= request.POST.get('listingposition')
                Property_Main_Category.objects.create(listing_type=listingtypeobj,Main_category=main_category_name,category_position=listingposition)
                return redirect('/propertymaincategory')

        else:
            return redirect('/propertymaincategory')

class EditPropertyMainCategory(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request,pk):
        propertymaincategoryobj=Property_Main_Category.objects.get(id=pk)
        propertylistingobj=Property_Listing_Type.objects.filter(is_active=True)
        context={"propertymaincategoryobj":propertymaincategoryobj,'propertylistingobj':propertylistingobj}
        return render(request,"edit-maincategory.html",context)

    def post(self, request,pk):
        maincategoryobj=Property_Main_Category.objects.get(id=pk)
        main_Category_name=request.POST.get('main_category_name')
        typeoflistingid=request.POST.get('typeoflisting')
        position=request.POST.get('position')
        is_active=request.POST.get('is_active')
        
        if main_Category_name:
            maincategoryobj.Main_category=main_Category_name
        if typeoflistingid:
            propertylistingtypeobject=Property_Listing_Type.objects.get(id=typeoflistingid)
            maincategoryobj.listing_type=propertylistingtypeobject
        if position:
            maincategoryobj.category_position=position
        if is_active:
            maincategoryobj.is_active=is_active
        
        maincategoryobj.save()

        return redirect('/propertymaincategory')

class PropertySubCategory(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request):
        maincategoryobj=Property_Main_Category.objects.filter(is_active=True)
        # Search
        if 'q' in request.GET:
            q=request.GET['q']
            multiple_q=Q(Q(property_sub_category_Name__icontains=q))
            multiple_p=Q(Q(Main_category__icontains=q))

            maincategoryobj=Property_Main_Category.objects.filter(multiple_p).values_list('id', flat=True)
            propertysubcategoryobj_type=Property_Sub_Category.objects.filter(property_main_category__in=maincategoryobj)
            propertysubcategoryobj_name=Property_Sub_Category.objects.filter(multiple_q)

            subcategorydata=list(chain(propertysubcategoryobj_type, propertysubcategoryobj_name))
        else:
            subcategorydata=Property_Sub_Category.objects.all()
        
        # Paginator
        paginator=Paginator(subcategorydata, 20)
        page_number=request.GET.get('page')
        subcategorydata=paginator.get_page(page_number)
        obj=paginator.page_range
        context={"maincategoryobj":maincategoryobj,'subcategorydata':subcategorydata,'obj':obj}
        return render(request,'Property_Sub_Category.html',context)
        # maincategoryobj=Property_Main_Category.objects.all()
        # subcategorydata=Property_Sub_Category.objects.all()
        # for i in subcategorydata:
        # context={"maincategoryobj":maincategoryobj,'subcategorydata':subcategorydata}
        # return render(request,'Property_Sub_Category.html',context)
    
    def post(self, request,id=None):
        if request.user.is_superuser:
            action=request.POST.get('action')
            if action=="Delete":
                if id!=None and Property_Sub_Category.objects.filter(id=id):
                    mainsubcategoryobj=Property_Sub_Category.objects.get(id=id)
                    mainsubcategoryobj.delete()
                    return redirect('/propertysubcategorylist')
                else:
                    return redirect('/propertysubcategorylist')
            else:
                propertytypelistinfid=request.POST.get('subcategoryid')
                maincategoryobj=Property_Main_Category.objects.get(id=propertytypelistinfid)
                sub_category_name=request.POST.get('sub_category_name')
                listingposition= request.POST.get('listingposition')
                Property_Sub_Category.objects.create(property_main_category=maincategoryobj,property_sub_category_Name=sub_category_name,category_position=listingposition)
                return redirect('/propertysubcategorylist')

        else:
            return redirect('/propertysubcategorylist')
 
class EditPropertySubCategory(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request,id):
        propertysubcategoryobj=Property_Sub_Category.objects.get(id=id)
        propertymaincategoryobj=Property_Main_Category.objects.filter(is_active=True)
        context={"propertymaincategoryobj":propertymaincategoryobj,'propertysubcategoryobj':propertysubcategoryobj}
        return render(request,"edit-subcategory.html",context)

    def post(self, request,id):
        subcategoryobj=Property_Sub_Category.objects.get(id=id)
        sub_Category_name=request.POST.get('sub_category_name')
        maincategoryid=request.POST.get('maincategory')
        position=request.POST.get('position')
        is_active=request.POST.get('is_active')
        
        if sub_Category_name:
            subcategoryobj.property_sub_category_Name=sub_Category_name
        if maincategoryid:
            propertymaincategoryobject=Property_Main_Category.objects.get(id=maincategoryid)
            subcategoryobj.property_main_category=propertymaincategoryobject
        if position:
            subcategoryobj.category_position=position
        if is_active:
            subcategoryobj.is_active=is_active
        
        subcategoryobj.save()

        return redirect('/propertysubcategorylist')

class PropertyType(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request):
        subcategoryobj=Property_Sub_Category.objects.filter(is_active=True)
        # Search
        if 'q' in request.GET:
            q=request.GET['q']
            multiple_q=Q(Q(proprty_type_name__icontains=q))
            multiple_p=Q(Q(property_sub_category_Name__icontains=q))

            propertysubcategoryobj=Property_Sub_Category.objects.filter(multiple_p).values_list('id',flat=True)
            propertytypeobj_type=Property_Type.objects.filter(property_sub_category__in=propertysubcategoryobj)
            propertytypeobj_name=Property_Type.objects.filter(multiple_q)
            
            propertytypeobj=list(chain(propertytypeobj_type,propertytypeobj_name))
        else:
            propertytypeobj=Property_Type.objects.all()
        
        # Paginator
        paginator = Paginator(propertytypeobj, 20)
        page_number = request.GET.get('page')
        propertytypeobj = paginator.get_page(page_number)
        obj = paginator.page_range

        context={'subcategoryobj':subcategoryobj,"propertytypeobj":propertytypeobj,'obj':obj}
        return render(request,"Property_Type.html",context)
        # subcategoryobj=Property_Sub_Category.objects.all()
        # propertytypeobj=Property_Type.objects.all()
        # context={'subcategoryobj':subcategoryobj,"propertytypeobj":propertytypeobj}
        # return render(request,"Property_Type.html",context)

    def post(self, request,id=None):
        if request.user.is_superuser:
            action=request.POST.get('action')
            if action=="Delete":
                if id!=None and Property_Type.objects.filter(id=id):
                    mainsubcategoryobj=Property_Type.objects.get(id=id)
                    mainsubcategoryobj.delete()
                    return redirect('/propertytype')
                else:
                    return redirect('/propertytype')
            else:
                subcategoryid=request.POST.get('subcategoryid')
                subcategoryobj=Property_Sub_Category.objects.get(id=subcategoryid)
                propertytypename=request.POST.get('propertytypename')
                posiiton= request.POST.get('posiiton')
                propertytypeimage= request.FILES.get('propertytypeimage')
                Property_Type.objects.create(property_sub_category=subcategoryobj,property_type_image=propertytypeimage,proprty_type_name=propertytypename,category_position=posiiton)
                return redirect('/propertytype')
        else:
            return redirect('/propertytype')
        
class EditPropertyType(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request,id):
        propertytypeobj=Property_Type.objects.get(id=id)
        propertysubcategoryobj=    Property_Sub_Category.objects.filter(is_active=True)
        context={"propertytypeobj":propertytypeobj,"propertysubcategoryobj":propertysubcategoryobj}
        return render(request,"edit-propertytype.html",context)

    def post(self, request,id):
        Propertytypeobj=Property_Type.objects.get(id=id)
        propertytype_name=request.POST.get('propertytype_name')
        property_type_image=request.FILES.get('property_type_image')
        subcategoryid= request.POST.get('subcategoryid')
        position=request.POST.get('position')
        is_active=request.POST.get('is_active')
        
        if propertytype_name:
            Propertytypeobj.proprty_type_name=propertytype_name
        if subcategoryid:
            propertysubcategoryobject=Property_Sub_Category.objects.get(id=subcategoryid)
            Propertytypeobj.property_sub_category=propertysubcategoryobject
        if position:
            Propertytypeobj.category_position=position
        if is_active:
            Propertytypeobj.is_active=is_active
        if property_type_image:
            Propertytypeobj.property_type_image=property_type_image
        Propertytypeobj.save()
        return redirect('/propertytype')

class PropertySettings(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request):

        return render(request, 'property-settings.html')

class LocationMaster(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request):

        return render(request, 'location-master.html')

class AdminPropertyAminites(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request):
        # Search
        if 'q' in request.GET:
            q=request.GET['q']
            multiple_q=Q(Q(amenities_name__icontains=q))
            Amenities_Masterobj=Amenities_Master.objects.filter(multiple_q)
        else:
            Amenities_Masterobj=Amenities_Master.objects.all()
        
        # paginator
        paginator=Paginator(Amenities_Masterobj,20)
        page_number=request.GET.get('page')
        Amenities_Masterobj=paginator.get_page(page_number)
        obj=paginator.page_range
        context={"Amenities_Masterobj":Amenities_Masterobj,'obj':obj}
        return render(request, 'Property_Aminity.html',context)
    
    def post(self, request):
        amenities_icon= request.FILES.get('amenity')
        amenities_name=request.POST.get('amenities_name')
        
        position=request.POST.get('position')
        Amenities_Master.objects.create(position=position,amenities_icon=amenities_icon,amenities_name=amenities_name,is_active=True)
        return redirect("/property-aminities")

class PropertyAminityDelete(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request,id):
        aminitymasterobj=Amenities_Master.objects.get(id=id)
        aminitymasterobj.delete()
        return redirect("/property-aminities")

class PropertyAminityEdit(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request,id):
        aminityobj=Amenities_Master.objects.get(id=id)
        context={'aminityobj':aminityobj}
        return render(request,"aminityedit.html",context)

    def post(self, request,id):
        aminityobj=Amenities_Master.objects.get(id=id)
        amenities_icon= request.FILES.get('aminity_image')
        amenities_name=request.POST.get('aminity_name')

        position=request.POST.get('position')
        is_active=request.POST.get('is_active')

        if amenities_icon:
            aminityobj.amenities_icon=amenities_icon
        if amenities_name:
            aminityobj.amenities_name=amenities_name    
        if position:
            aminityobj.position = position
        if is_active:
             aminityobj.is_active=is_active
        aminityobj.save()
        return redirect("/property-aminities")

class SubscriptionServicesView(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request):
        if 'q' in request.GET:
            q = request.GET['q']
            multiple_q=Q(Q(service_name__icontains=q))
            serviceobj=SubscriptionServices.objects.filter(multiple_q)
        else:
            serviceobj=SubscriptionServices.objects.all()
        
        paginator = Paginator(serviceobj,10)
        page_number=request.GET.get('page')
        serviceobj=paginator.get_page(page_number)
        # print(serviceobj)
        obj=paginator.page_range
        context={"serviceobj":serviceobj,"obj":obj}
        return render(request, 'Subscription_services.html',context)

    def post(self, request):
        usertype=request.POST.get('user_type')
        servicename=request.POST.get('servicename')
        position= request.POST.get('position')
        SubscriptionServices.objects.create(usertype=usertype,service_name=servicename,position=position)
        return redirect('/subscription-services')

class DeleteSubscriptionService(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request, id):
        deletesubscriptionservice=SubscriptionServices.objects.filter(id=id)
        deletesubscriptionservice.delete()
        return redirect('/subscription-services')

class EditSubscriptionServices(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request,id):
        subscriptionservicesobj=SubscriptionServices.objects.get(id=id)
        context={"subscriptionservicesobj":subscriptionservicesobj}
        return render(request, 'edit-subscriptionservice.html', context)
    def post(self, request,id):
        subscriptionservicesobj=SubscriptionServices.objects.get(id=id)
        service_name=request.POST.get('service_name')
        posiiton=request.POST.get('position')
        is_active=request.POST.get('is_active')

        if service_name:
            subscriptionservicesobj.service_name=service_name
        if posiiton:
            subscriptionservicesobj.position=posiiton
        if is_active:
            subscriptionservicesobj.is_active=is_active 
        subscriptionservicesobj.save()
    
        return redirect('/subscription-services')


class SubscriptionPlanView(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request, id=None):
        if id == None:
            if 'q' in request.GET:
                q = request.GET['q']
                multiple_q=Q(Q(Name__icontains = q) | Q(plan_type__icontains = q))
                subscriptionplanobj=SubscriptionPlanServices.objects.filter(multiple_q)
            else:
                subscriptionplanobj=SubscriptionPlanServices.objects.all()
            
            subscriptionservicesobj=SubscriptionServices.objects.filter(is_active=True)
            propertytypeobj=Propertylisting_type.objects.all()
            propertylistingtypeobj=Property_Listing_Type.objects.all()
            paginator=Paginator(subscriptionplanobj,4)
            page_number=request.GET.get('page')
            subscriptionplanobj=paginator.get_page(page_number)
            obj=paginator.page_range
            context={"propertytypeobj":propertytypeobj,"propertylistingtypeobj":propertylistingtypeobj,"subscriptionservicesobj":subscriptionservicesobj,'subscriptionplanobj':subscriptionplanobj,'obj':obj}
            return render(request, 'Subscription_plan.html',context)
        else:
            subscribeplanobjupdate=SubscriptionPlanServices.objects.get(id=id)
            subscribeplanobjupdate.delete()
            return redirect('/subscription-plan')
    
    def post(self, request, id=None):
        
        user_type= request.POST.get('user_type')
        name=request.POST.get('name')
        plan_type= request.POST.get('plan_type')
        monthly_price= request.POST.get('monthly_price')
        yearly_price= request.POST.get('yearly_price')
        discount_type= request.POST.get('discount_type')
        discount= request.POST.get('discount')
        discountmininumseat= request.POST.get('discountmininumseat')
        titles=request.POST.get('titles')
        serives=request.POST.getlist('services')
        # print(serives)
        listingtype=request.POST.get('listingtype')
        allow_listing=request.POST.get('allow_listing')
        
        l=[]
        
        subscriptionserviceobj=SubscriptionServices.objects.filter(usertype=2)

        for i in subscriptionserviceobj:
            # print(i.id)
            d={}
            if str(i.id) in serives:
                d["lable"]=i.service_name
                d['status']=True
            else:
                d["lable"]=i.service_name
                d['status']=False
            l.append(d)

        if allow_listing != None:
            Total_listing=request.POST.get('total_listing')
            propertylistingtype=request.POST.getlist('property_type')
            propertylistingtypeobj=request.POST.getlist('propertylistingobj')

            subscribeplanobj=SubscriptionPlanServices.objects.create(
                UserType=user_type ,Name=name ,plan_type=plan_type ,monthly_price=monthly_price , 
                yearly_price=yearly_price ,discounttype=discount_type ,discount=discount , 
                discountmininumseat=discountmininumseat ,titles=titles, subscriptionservices=serives,
                total_listing=Total_listing ,propertype=propertylistingtype ,properlisting=propertylistingtypeobj,
                listing_type=listingtype,Subscription_services=l
                )
            # subscribeplanobj.save()    
        else:
            subscribeplanobj=SubscriptionPlanServices.objects.create(
                UserType=user_type ,Name=name ,plan_type=plan_type ,monthly_price=monthly_price , 
                yearly_price=yearly_price ,discounttype=discount_type ,discount=discount , 
                discountmininumseat=discountmininumseat ,subscriptionservices=serives,Subscription_services=l
                )
        return redirect('/subscription-plan')
    
class SubscriptionPlanUpdate(View):
    def get(self, request, id):
        subscribeplanobjupdate=SubscriptionPlanServices.objects.get(id=id)
        if SubscriptionServices.objects.filter(id__in=subscribeplanobjupdate.subscriptionservices):
            subscriptionservicesobj=SubscriptionServices.objects.filter(id__in=subscribeplanobjupdate.subscriptionservices)
        else:
            subscriptionservicesobj=None
        subscriptionservicesobj1=SubscriptionServices.objects.exclude(id__in=subscribeplanobjupdate.subscriptionservices).filter(is_active=True)

        if Propertylisting_type.objects.filter(id__in=subscribeplanobjupdate.propertype):
            propertytypeobj=Propertylisting_type.objects.filter(id__in=subscribeplanobjupdate.propertype)
        else:
            propertytypeobj=None
            
        propertytypeobj1=Propertylisting_type.objects.exclude(id__in=subscribeplanobjupdate.propertype)
        propertylistingtypeobj=Property_Listing_Type.objects.all()
        context={'propertytypeobj1':propertytypeobj1,'subscriptionservicesobj1':subscriptionservicesobj1,'subscribeplanobjupdate':subscribeplanobjupdate,"propertytypeobj":propertytypeobj,"propertylistingtypeobj":propertylistingtypeobj,"subscriptionservicesobj":subscriptionservicesobj}
        return render(request, 'edit_Subscription_plan.html', context)
    
    def post(self, request, id):
        subscribeplanobjupdate=SubscriptionPlanServices.objects.get(id=id)
        # subscribeplanobjupdate.UserType=request.POST.get('user_type')
        # subscribeplanobjupdate.Name=request.POST.get('name')
        # subscribeplanobjupdate.plan_type=request.POST.get('plan_type')
        subscribeplanobjupdate.monthly_price=request.POST.get('monthly_price')
        subscribeplanobjupdate.yearly_price=request.POST.get('yearly_price')
        subscribeplanobjupdate.discounttype=request.POST.get('discount_type')
        subscribeplanobjupdate.discount=request.POST.get('discount')
        subscribeplanobjupdate.titles=request.POST.get('titles')

        # subscribeplanobjupdate.discountmininumseat=request.POST.get('discountmininumseat')
        subscribeplanobjupdate.subscriptionservices=request.POST.getlist('services')
        # subscribeplanobjupdate.total_listing=request.POST.get('total_listing')
        # subscribeplanobjupdate.propertype=request.POST.getlist('property_type')
        # subscribeplanobjupdate.properlisting=request.POST.getlist('propertylistingobj')
        subscribeplanobjupdate.save()
        return redirect('/subscription-plan')
  
  
class AgentLicView(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request):
        # serach
        if 'q' in request.GET:
            q=request.GET['q']
            multiple_q=Q(Q(license_number__icontains=q) | Q(Full_name__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q)) 
           
            # multiple_p=Q(Q(is_validated__icontains=q))
            agentlicobj=AgentLic.objects.filter(multiple_q)
        else:
            agentlicobj=AgentLic.objects.all()

        # paginator
        paginator=Paginator(agentlicobj,20)
        page_number=request.GET.get('page')
        agentlicobj=paginator.get_page(page_number)
        obj=paginator.page_range
        context={"agentlicobj":agentlicobj, "obj":obj}
        return render(request, 'Agent-Lic.html',context)
    
    def post(self, request):
        dataset = Dataset()
        file = request.FILES['myfile']
        imported_data = dataset.load(file.read(),format='xlsx')
        for data in imported_data:
            try:
                value = AgentLic(license_number=data[0],Full_name=data[1],first_name=data[2],last_name=data[3],is_validated=False)
                value.save()
            except:
                pass    
        return redirect('/agentlicview')
    
class AgentLicDelete(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request, id=None):
        agentlic = AgentLic.objects.get(id=id)
        agentlic.delete()
        return redirect("/agentlicview")

# class AddLocation(View):
#     def post(self, request):
#         dataset = Dataset()
#         file = request.FILES['myfile']
#         imported_data = dataset.load(file.read(),format='xlsx')
#         for data in imported_data:
#             if CountryMaster.objects.filter(country_name=data[0]).exists():
#                 CountryMasterobj=CountryMaster.objects.filter(country_name=data[0]).last()
#             else:
#                 CountryMasterobj = CountryMaster.objects.create(
#                     country_code = data[1], country_name = data[0]
#                 )
            
#             if StateMaster.objects.filter(state_name = data[2]).exists():
#                 statemasterobj = StateMaster.objects.filter(state_name = data[2]).last()
#             else:
#                 statemasterobj = StateMaster.objects.create(
#                     country_master = CountryMasterobj, state_name = data[2]
#                 )
            
#             if CityMaster.objects.filter(city_name = data[3]).exists():
#                 citymasterobj = CityMaster.objects.filter(city_name = data[3]).last()
#             else:
#                 citymasterobj = CityMaster.objects.create(
#                     state_master = statemasterobj, city_name = data[3]
#                 )
            
#             if AreaMaster.objects.filter(area_name= data[4]).exists():
#                 areamasterobj = AreaMaster.objects.filter(area_name= data[4]).last()
#             else:
#                 areamasterobj = AreaMaster.objects.create(
#                 city_master = citymasterobj, area_name= data[4], prefered_name= data[5]
#                 )
            
#             zipcodeobj = ZipCodeMaster.objects.create(
#                 area_master = areamasterobj, Zipcode = data[6]
#             )
            
#         return redirect("/location-master")

class AddLocation(View):
    def post(self, request):
        dataset = Dataset()
        file = request.FILES.get('myfile')
        imported_data = dataset.load(file.read(), format = 'xlsx')
        for i in imported_data:
            if CountryMaster.objects.filter(country_name=i[0]).exists():
                CountryMasterobj = CountryMaster.objects.get(country_name=i[0])
            else:
                CountryMasterobj = CountryMaster.objects.create(country_name=i[0], country_code = i[1],position = i[2])
            
            if StateMaster.objects.filter(state_name = i[3]).exists():
                StateMasterobj = StateMaster.objects.get(state_name = i[3])
            else:
                StateMasterobj = StateMaster.objects.create(state_name = i[3], country_master = CountryMasterobj, position = i[4])
            
            if CityMaster.objects.filter(state_master = StateMasterobj, city_name = i[5]).exists():
                CityMasterobj = CityMaster.objects.filter(state_master = StateMasterobj).get(city_name = i[5])
            else:
                CityMasterobj = CityMaster.objects.create(state_master = StateMasterobj, city_name = i[5], position = i[6])
            
            if AreaMaster.objects.filter(city_master = CityMasterobj, area_name = i[7]).exists():
                AreaMasterobj = AreaMaster.objects.filter(city_master = CityMasterobj).get(area_name = i[7])
            else:
                AreaMasterobj = AreaMaster.objects.create(city_master = CityMasterobj, area_name = i[7], prefered_name = i[8], position = i[9])
            
            zipcodeobj = ZipCodeMaster.objects.create(
                area_master = AreaMasterobj, Zipcode = i[10], position = i[11]
            )
        return redirect("/GeoDataBasePage")

from itertools import chain
class StateMasterView(View):
    def get(self, request):
        countrymasterobj=CountryMaster.objects.filter(is_active=True)
        # serach
        if 'q' in request.GET:
            q=request.GET['q']
            multiple_q=Q(Q(state_name__icontains=q))
            multiple_p=Q(Q(country_name__icontains=q))

            countrymasterobj=CountryMaster.objects.filter(multiple_p).values_list('id',flat=True)
            statemasterobj_country=StateMaster.objects.filter(country_master__in=countrymasterobj)
            statemasterobj_name=StateMaster.objects.filter(multiple_q)

            result_list = list(chain(statemasterobj_country, statemasterobj_name))
        else:
            result_list=StateMaster.objects.all()
        # paginator
        paginator=Paginator(result_list,10)
        page_number=request.GET.get('page')
        result_list=paginator.get_page(page_number)
        obj=paginator.page_range
        context={"countrymasterobj":countrymasterobj,"result_list":result_list, "obj":obj}
        return render(request,'StateMaster.html',context)

    def post(self, request):
        country_id=request.POST.get('country_id')
        countryobj=CountryMaster.objects.get(id=country_id)
        state_name=request.POST.get('state_name')
        position=request.POST.get('position')
        StateMaster.objects.create(country_master=countryobj,state_name=state_name,position=position)
        return redirect('/statemaster')

class DeleteStateMasterView(View):
    def post(self, request,id):
        statemasterobj=StateMaster.objects.get(id=id)
        statemasterobj.delete()
        return redirect('/statemaster')

class EditStateMasterView(View):
    def get(self, request,id):
        countrymasterobj=CountryMaster.objects.filter(is_active=True)
        statemasterobj=StateMaster.objects.get(id=id)
        context={"statemasterobj":statemasterobj,"countrymasterobj":countrymasterobj}
        return render(request,'edit-statemaster.html',context)
    
    def post(self, request,id):
        country_id=request.POST.get('country_id')
       
        state_name=request.POST.get('state_name')
        position=request.POST.get('position')
        is_active=request.POST.get('is_active')

        statemasterobj=StateMaster.objects.get(id=id)
        if country_id:   
            countrymasterobj=CountryMaster.objects.get(id=country_id)
            statemasterobj.country_master=countrymasterobj
        if state_name:
            statemasterobj.state_name=state_name
        if position:
            statemasterobj.position=position
        if is_active:
            statemasterobj.is_active=is_active
        statemasterobj.save()
        return redirect('/statemaster')

class CityMasterView(View):
    def get(self, request):
        statemasterobj=StateMaster.objects.filter(is_active=True)
        # search
        if 'q' in request.GET:
            q=request.GET['q']
            multiple_q=Q(Q(city_name__icontains=q)) 
            multiple_p=Q(Q(state_name__icontains=q))

            statemasterobj=StateMaster.objects.filter(multiple_p).values_list('id', flat=True)
            citymasterobj_state=CityMaster.objects.filter(state_master__in=statemasterobj)
            citymasterobj_name=CityMaster.objects.filter(multiple_q)

            citymasterobj=list(chain(citymasterobj_state, citymasterobj_name))
        else: 
            citymasterobj=CityMaster.objects.all()

        # paginator
        paginator=Paginator(citymasterobj,10)
        page_number=request.GET.get('page')
        citymasterobj=paginator.get_page(page_number)
        obj=paginator.page_range
        context={"citymasterobj":citymasterobj,"statemasterobj":statemasterobj, "obj":obj}
        return render(request,'CityMaster.html',context)

    def post(self, request):
        state_id=request.POST.get('state_id')
        statobj=StateMaster.objects.get(id=state_id)
        image=request.FILES.get('city')
        city_name=request.POST.get('city_name')
        position=request.POST.get('position')
        CityMaster.objects.create(state_master=statobj,city_image=image,city_name=city_name,position=position)
        return redirect('/citymaster')

class EditCityMasterView(View):
    def get(self, request,id):
        statemasterobj=StateMaster.objects.filter(is_active=True)
        citymasterobj=CityMaster.objects.get(id=id)
        context={"statemasterobj":statemasterobj,"citymasterobj":citymasterobj}
        return render(request,'edit-citymaster.html',context)
    
    def post(self, request,id):
        state_id=request.POST.get('state_id')
        image=request.FILES.get('city_image')
        city_name=request.POST.get('city_name')
        position=request.POST.get('position')
        is_active=request.POST.get('is_active')

        citymasterobj=CityMaster.objects.get(id=id)
        if image:
            citymasterobj.city_image=image
        if state_id:   
            statemasterobj=StateMaster.objects.get(id=state_id)
            citymasterobj.state_master=statemasterobj
            # print(statemasterobj)
        if city_name:
            citymasterobj.city_name=city_name
            # print(city_name)
        if position:
            citymasterobj.position=position
        if is_active:
            citymasterobj.is_active=is_active
        citymasterobj.save()
        return redirect('/citymaster')

class DeleteCityMasterView(View):
    def post(self, request,id):
        citymasterobj=CityMaster.objects.get(id=id)
        citymasterobj.delete()
        return redirect('/citymaster')

class Uploadlanguage(View):
    def post(self, request):
        dataset = Dataset()
        file = request.FILES['myfile']
        imported_data = dataset.load(file.read(),format='xlsx')
        for data in imported_data:
            value = LanguageMaster.objects.create(languages_name=data[0],position=data[1]) 
        return redirect('/languagemaster')



class EditLanguageMasterView(View):
    def get(self, request,id):
        languagemasterobj=LanguageMaster.objects.get(id=id)
        context={"languagemasterobj":languagemasterobj}
        return render(request,'edit-languagemaster.html',context)
    
    def post(self, request,id):
        language_name=request.POST.get('language_name')
        position=request.POST.get('position')
       
        languagemasterobj=LanguageMaster.objects.get(id=id)
       
        if language_name:
            languagemasterobj.languages_name=language_name
        if position:
            languagemasterobj.position=position
        
        languagemasterobj.save()
        return redirect('/languagemaster')

# class DeleteCityMasterView(View):
#     def post(self, request,id):
#         citymasterobj=CityMaster.objects.get(id=id)
#         citymasterobj.delete()
#         return redirect('/citymaster')

def superuserregistrations(request):
    if request.method == "POST":
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        email=request.POST.get('email')
        password=request.POST.get('password')

        userobj=User.objects.create_user(email=email, password=password,username=email, is_active=True, is_email_verified=True, is_superuser=True, is_staff=True)
        usertypeobj=UserType.objects.create(user=userobj,user_type=0)
        UserProfile.objects.create(user_type=usertypeobj,first_name=firstname,last_name=lastname)
        return redirect('/')
    return render(request,"sign-up.html")

class Agent_Lic_Pending_Reuqest(View):
    def get(self, request):
        # Serach
        if 'q' in request.GET:
            q=request.GET['q']
            multiple_q=Q(Q(license_number__icontains=q) | Q(Full_name__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q)) 
            pending_request = AgentLic.objects.filter(multiple_q).filter(is_requested=True)
        else:
           pending_request = AgentLic.objects.filter(is_requested=True)
           
        paginator=Paginator(pending_request,20)
        page_number=request.GET.get('page')
        pending_request=paginator.get_page(page_number)
        obj=paginator.page_range
        context = {'agentlicobj':pending_request, "obj":obj}
        return render(request, "Agent-Lic-pending-requested.html", context)
    
    def post(self, request, id):
        agentlicobj=AgentLic.objects.get(id=id)
        requestobj=request.POST.get('action')
        if requestobj == 'Approve':
            agentlicobj.is_validated=True
            agentlicobj.lic_already_use=True
            agentlicobj.is_requested=False
            agentlicobj.is_rejected=False
            agentlicobj.save()
            UserTypeobj=UserType.objects.get(user=agentlicobj.user.id)
            userprofileobj=UserProfile.objects.get(user_type=UserTypeobj)
            userprofileobj.brokerage_name=agentlicobj.Full_name
            userprofileobj.sales_persones_license=agentlicobj.license_number
            userprofileobj.agent_broker_license_title=agentlicobj.lic_Type
            userprofileobj.save()
            agentobj = AgentApprovedSubscriptionPlan.objects.filter(user= agentlicobj.user)
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
        else:
            agentlicobj.is_rejected=True
            agentlicobj.is_validated=False
            agentlicobj.lic_already_use=False
            agentlicobj.is_requested=True
            agentlicobj.user=None
            agentlicobj.save()
        return redirect('/agentpendingrequest')

class Agent_Lic_Approved_Reuqest(View):
    def get(self, request):
        # Search
        if 'q' in request.GET:
            q=request.GET['q']
            multiple_q=Q(Q(license_number__icontains=q) | Q(Full_name__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q)) 
            approved_request = AgentLic.objects.filter(multiple_q).filter(is_validated=True)
        else:
            approved_request = AgentLic.objects.filter(is_validated=True)
        
         # paginator
        paginator=Paginator(approved_request,20)
        page_number=request.GET.get('page')
        approved_request=paginator.get_page(page_number)
        obj=paginator.page_range
        context = {'agentlicobj':approved_request,'obj':obj}
        return render(request, "Agent-Lic-Approve.html", context)

class Neighborhood_Approved(View):
    def get(self,request):
        approve_request = Nb_specality_area.objects.all().exclude(is_verified = "Pending")
        area = AreaMaster.objects.all()
        context = {'neighborhood':approve_request,"area":area}
        return render(request, "Agent-Neighborhood-Approve.html", context)

class Agent_Neighborhood_Specialist_Panding_request(View):
    def get(self, request):
        pending_request = Nb_specality_area.objects.filter(is_requested=True)
        area = AreaMaster.objects.all()
        context = {'neighborhood':pending_request,"area":area}
        return render(request, "Agent-neighborhood-pending-requested.html", context)

    def post(self, request, id):
        neighborhood = Nb_specality_area.objects.get(id =id)
        requestobj=request.POST.get('action')
        if requestobj == 'Approve':
            neighborhood.is_requested = False
            neighborhood.is_verified = "Approve"
            neighborhood.save()
        else:
            neighborhood.is_requested = False
            neighborhood.is_verified = "Reject"
            neighborhood.save()
        return redirect("neighborhoodpendingrequest")

# Luxary Amount
class luxarysalesamt(View):
    def get(self, request, id=None):
        if id==None:
            salesobj=LuxarySalesAmt.objects.all()
            context={'salesobj':salesobj}
            return render(request, 'luxarysalesamount.html', context)
        else:
            salesobj=LuxarySalesAmt.objects.get(id=id)
            salesobj.delete()
            return redirect('/luxarysalesamt')
    def post(self ,request):
        salesamount=request.POST.get('amount')
        LuxarySalesAmt.objects.create(Amt=salesamount)
        return redirect('/luxarysalesamt')

class luxaryrentamt(View):
    def get(self, request, id=None):
        if id==None:
            rentobj=LuxaryRentAmt.objects.all()
            context={'rentobj':rentobj}
            return render(request, 'luxaryrentamount.html', context)
        else:
            rentobj=LuxaryRentAmt.objects.get(id=id)
            rentobj.delete()
            return redirect('/luxaryrentamt')
    def post(self ,request):
        rentamount=request.POST.get('amount')
        LuxaryRentAmt.objects.create(Amt=rentamount)
        return redirect('/luxaryrentamt')

class BoostMarketingAdminAll(View):
    @method_decorator(login_required(login_url='/'))
    def get(self,request):
        boostmarketingadmin=UserType.objects.filter(user_type=7).values_list("id",flat=True)
        userprofile=UserProfile.objects.filter(user_type_id__in=boostmarketingadmin)
        paginator=Paginator(userprofile,20)
        page_number=request.GET.get('page')
        boostmarketingadmin=paginator.get_page(page_number)
        obj=paginator.page_range
        context={'userprofile':boostmarketingadmin, "obj":obj}
        # print('yes',"NO")
        return render(request,'allboostmarketingadmin.html',context)
    
    def post(self, request):
        user=request.user
        obj=BoostMarketingServicesTOUser.objects.filter(user=user)
        for i in obj:
            i.is_active=False
            i.save()
        user.is_Active=False
        user.save()
        return redirect('/allboostmarketingadmin')

from accounts.profilepasswordviews import decrypt,encrypt
key = '01234567890123456789015545678901'
from accounts import utils 
class AddBoostmarketingAdmin(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request):
        boostmarketingobj=BoostMarketingServicesTOUser.objects.filter(is_active=True).values_list('ServiceNumber',flat=True)
        context={'boostmarketingobj':boostmarketingobj}
        return render(request,"boostmarketingadminadd.html",context)
    
    def post(self, request):
            # print(request.POST)
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            email=request.POST.get('email')
            password = request.POST.get('password')
            # password = secrets.token_hex(16)
            encrypted_string = encrypt(key, password)

            work_number=request.POST.get('work_number')
            short_description=request.POST.get('short_description')
            select_service=request.POST.getlist('select_service')
            profile=request.FILES.get('profile')
            # print(select_service)
            if User.objects.filter(username=email):
                # print("email already in use")
                return redirect("/AddBoostmarketingAdmin/")
            else:
                userobj=User.objects.create(email=email, username=email, password=encrypted_string,is_active=True)
                # print('user : ', userobj)
                usertype=UserType.objects.create(user=userobj,user_type=7)
                # print('user type : ', usertype)
                UserProfile.objects.create(user_type=usertype,first_name=first_name,last_name=last_name,work_number_1=work_number,personal_bio=short_description,unique_id='boost')
                for item in select_service:
                    BoostMarketingServicesTOUser.objects.create(user=userobj, ServiceNumber=item)
                
                passwordobj = decrypt(key, userobj.password)
                current_site = get_current_site(request).domain
                absurl = 'http://dev.api.MLS-tutor.com/Boost-Marketing-Admin-Login/'
                email_body = 'Hi '+userobj.username + \
                ' Use the link below to verify your email \n' + absurl +'\n'+"username = "+ userobj.email+'\n'+"password = "+passwordobj
                data = {'email_body': email_body, 'to_email': userobj.username,'email_subject': 'Verify your email',
                        "username": userobj.email, "password":passwordobj}
                Util.send_email(data)
                return redirect("/AddBoostmarketingAdmin/")

class DeleteBoostMarketingAdmin(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request, id):
        user = User.objects.get(id=id)
        user.delete()
        return redirect('BoostMarketingAdminAll')

class Property_list_view(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request):
        if 'q' in request.GET:
            q = request.GET['q']
            multiple_q=Q(property_title__icontains=q)
            propertyobj=Property_Detail.objects.filter(multiple_q)
        else:
            propertyobj=Property_Detail.objects.all()
        # Pagination
        paginator=Paginator(propertyobj, 20)
        page_number=request.GET.get('page')
        propertyobj=paginator.get_page(page_number)
        obj=paginator.page_range
        context={"propertyobj":propertyobj,"obj":obj}
        return render(request, 'property-detail-list.html', context )

class DetailView(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request, id):
        propertyobj=Property_Detail.objects.get(id=id)
        context={"propertyobj":propertyobj}
        return render(request, 'property-profile.html', context)

class AgentSupportView(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request):
        usertype = UserType.objects.filter(user_type = 2)
        user = []
        for i in usertype:
            user.append(i.user.id)
        support = SupportTickets.objects.filter(user__in = user, is_request = True)
        context = {'support': support}
        return render(request, 'AgentSupport.html', context)

    def post(self, request, id):
        support = SupportTickets.objects.get(id = id)
        requestobj=request.POST.get('action')
        if requestobj == 'Approve':
            support.status = True
        else:
            support.status = False
        support.is_request = False
        support.save()
        return redirect("/AgentSupportView")


class GuestSupportView(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request):
        usertype = UserType.objects.filter(user_type = 1)
        user = []
        for i in usertype:
            user.append(i.user.id)
        support = SupportTickets.objects.filter(user__in = user, is_request = True)
        context = {'support': support}
        return render(request, 'GuestSupport.html', context)

    def post(self, request, id):
        support = SupportTickets.objects.get(id = id)
        requestobj=request.POST.get('action')
        if requestobj == 'Approve':
            support.status = True
        else:
            support.status = False
        support.is_request = False
        support.save()
        return redirect("/GuestSupportView")

# =================================================================================================================================================================
# ================================================================ NewTemplate ===================================================================================
# =================================================================================================================================================================


class AdminDashboard(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request):
        # All
        suppoetobj = SupportTickets.objects.all().count()
        # Agent
        usertype = UserType.objects.filter(user_type = 2).values_list('user', flat=True)
        agentsupportobj = SupportTickets.objects.filter(user__in = usertype).count()
        # Guest
        usertype = UserType.objects.filter(user_type = 1).values_list('user', flat=True)
        guestsupportobj = SupportTickets.objects.filter(user__in = usertype).count()
        return render(request, 'NewTemplate/Dashboard.html', locals())

class ProfilePage(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request):
        # all
        user = User.objects.all().exclude(is_superuser = True)
        usertype0obj = UserType.objects.filter(user__in = user).values_list("id", flat=True)
        userprofilecount = UserProfile.objects.filter(user_type__in = usertype0obj).count()
        # Agent
        usertypeobj = UserType.objects.filter(user_type = 2)
        agentprofilecount = UserProfile.objects.filter(user_type__in = usertypeobj).count()
        # Guest
        usertypeobj1 = UserType.objects.filter(user_type = 1)
        guestprofilecount = UserProfile.objects.filter(user_type__in = usertypeobj1).count()
        # Investor
        usertypeobj2 = UserType.objects.filter(user_type = 3)
        investorprofilecount = UserProfile.objects.filter(user_type__in = usertypeobj2)
        # print(investorprofilecount)
        nbpendingcount = Nb_specality_area.objects.filter(is_verified="Pending").count()

        licobj = AgentLic.objects.filter(is_validated = False, is_requested = True).count()
        # BoostMarketing Admin
        boostmarketingobj=BoostMarketingServicesTOUser.objects.filter(is_active=True).values_list('ServiceNumber',flat=True)
        return render(request, 'NewTemplate/Profile.html', locals())

class GeoDataBasePage(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request):
        # # Dependenci
        propety_listing_type=Propertylisting_type.objects.all()
        # # Property Listing Data
        propertylistingtypeobj=Property_Listing_Type.objects.all()
        # propertymaincategoryobj=Property_Main_Category.objects.all()
        # subcategorydata=Property_Sub_Category.objects.all()
        # # location Data
        # # Country Data
        propetyexcelfileobj = Propetyexcelfile.objects.last()
        loactionexcelobj = Locationexcelfile.objects.last()

        countrymasterobj = CountryMaster.objects.all()
        # # state data
        statemasterobj = StateMaster.objects.all()
        # # City data
        citymasterobj = CityMaster.objects.all()
        # # town
        # areaobj = AreaMaster.objects.all()
        # # zip
        # zipcode = ZipCodeMaster.objects.all()
        return render(request, 'NewTemplate/GeoDatabase.html', locals())

# Property Type
class AddPropertyLIstingTypeView(View):
    @method_decorator(login_required(login_url='/'))
    def post(self, request):
        type_of_listing=request.POST.get('type_of_listing')
        propertytypelistingobj=Propertylisting_type.objects.get(id=type_of_listing)
        listing_type=request.POST.get('listing_type')
        user_listing_type = request.POST.get("user_listing_type")
        listingposition= request.POST.get('listingposition')
        Property_Listing_Type.objects.create(type_of_listing=propertytypelistingobj,listing_type=listing_type,listing_position=listingposition,user_listing_type=user_listing_type)
        return redirect('/GeoDataBasePage')

# Property Main Category
class AddPropertyMainCategoeryView(View):
    @method_decorator(login_required(login_url='/'))
    def post(self, request):
        propertytypelistinfid=request.POST.get('maincategoryid')
        listingtypeobj=Property_Listing_Type.objects.get(id=propertytypelistinfid)
        main_category_name=request.POST.get('main')
        listingposition= request.POST.get('listingposition')
        Property_Main_Category.objects.create(listing_type=listingtypeobj,Main_category=main_category_name,category_position=listingposition)
        return redirect('/GeoDataBasePage')
    
# Property Sub Category
class AddPropertySubCategoryView(View):
    @method_decorator(login_required(login_url='/'))
    def post(self, request):
        propertytypelistinfid=request.POST.get('subcategoryid')
        maincategoryobj=Property_Main_Category.objects.get(id=propertytypelistinfid)
        sub_category_name=request.POST.get('sub_category_name')
        listingposition= request.POST.get('listingposition')
        Property_Sub_Category.objects.create(property_main_category=maincategoryobj,property_sub_category_Name=sub_category_name,category_position=listingposition)
        return redirect('/GeoDataBasePage')

class AddTermsView(View):
    @method_decorator(login_required(login_url='/'))
    def post(self, request):
        listingmain = request.POST.get('listingmain')
        listingobj = Propertylisting_type.objects.get(id = listingmain)
        account_type = request.POST.get('account_type')
        listingsub = request.POST.get('sublistingtype')
        sublisting = Property_Listing_Type.objects.get(id = listingsub)
        terms = request.POST.get('trems')
        position = request.POST.get('position')
        termsobj = Terms.objects.create(
            property_listing_type = listingobj,
            propertylisting_type = sublisting,
            usertypeobj = account_type,
            terms = terms,
            position = position
        )
        return redirect('/Toolspage')
    
class AddOffersView(View):
    @method_decorator(login_required(login_url='/'))
    def post(self, request):
        listingmain = request.POST.get('listingmain')
        listingobj = Propertylisting_type.objects.get(id = listingmain)
        account_type = request.POST.get('account_type')
        listingsub = request.POST.get('sublistingtype')
        sublisting = Property_Listing_Type.objects.get(id = listingsub)
        offer = request.POST.get('Offer')
        position = request.POST.get('position')
        termsobj = Offer.objects.create(
            property_listing_type = listingobj,
            propertylisting_type = sublisting,
            usertypeobj = account_type,
            offer = offer,
            position = position
        )
        return redirect('/Toolspage')

class SublistingView(View):
    def get(self, request):
        listingmain = request.GET.get('listingmain')
        listingobj = Propertylisting_type.objects.get(id = listingmain)
        sublisting = Property_Listing_Type.objects.filter(type_of_listing = listingobj)
        return render(request, 'NewTemplate/listingsub.html', {'sublisting':sublisting})

class MainCategorylisting(View):
    def get(self, request):
        sublistingmain = request.GET.get('sublistingmain')
        sublistingobj = Property_Listing_Type.objects.get(id = sublistingmain)
        maincategoryobj = Property_Main_Category.objects.filter(listing_type = sublistingobj)
        # print(maincategoryobj)
        return render(request, 'NewTemplate/maincategorylisting.html', {'maincategoryobj':maincategoryobj})

class Toolspage(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request):
        # Terms data
        propety_listing_type=Propertylisting_type.objects.all()
        # termsobj = Terms.objects.all()
        hometitleobj = HomeCardTitle.objects.all()
        return render(request, 'NewTemplate/MLS-tutor-tools.html', locals())

class VerficationDashboard(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request):
        agentlicobj=AgentLic.objects.all()[::-1]
        pending_request = Nb_specality_area.objects.filter(is_requested=True)[::-1]
        area = AreaMaster.objects.all()
        context={"agentlicobj":agentlicobj,'neighborhood':pending_request,"area":area}
        return render(request, 'NewTemplate/VerficationDashboard.html', context)

class BoostMarketingAdminDashBoard(View):
    def get(self, request):
        boostmarketingadmin=UserType.objects.filter(user_type=7).values_list("id",flat=True)
        userprofile=UserProfile.objects.filter(user_type_id__in=boostmarketingadmin)
        context={'userprofile':userprofile}
        return render(request, 'NewTemplate/BoostMarketingDashboard.html',context)

class BoosMarketingAddAdmin(View):
    def get(self, request):
        boostmarketingobj=BoostMarketingServicesTOUser.objects.filter(is_active=True).values_list('ServiceNumber',flat=True)
        context={'boostmarketingobj':boostmarketingobj}
        return render(request, 'NewTemplate/Boostmarketing-adminadd.html',context)

    def post(self, request):
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        password = request.POST.get('password')
        # password = secrets.token_hex(16)
        encrypted_string = encrypt(key, password)

        work_number=request.POST.get('work_number')
        short_description=request.POST.get('short_description')
        select_service=request.POST.getlist('select_service')
        profile=request.FILES.get('profile')
        if User.objects.filter(username=email):
            return redirect("/AddBoostmarketingAdmin/")
        else:
            userobj=User.objects.create(email=email, username=email, password=encrypted_string,is_active=True)
            usertype=UserType.objects.create(user=userobj,user_type=7)
            UserProfile.objects.create(user_type=usertype,first_name=first_name,last_name=last_name,work_number_1=work_number,personal_bio=short_description,unique_id='boost')
            for item in select_service:
                BoostMarketingServicesTOUser.objects.create(user=userobj, ServiceNumber=item)
            
            passwordobj = decrypt(key, userobj.password)
            current_site = get_current_site(request).domain
            absurl = 'http://'+current_site+'/Boost-Marketing-Admin-Login/'
            email_body = 'Hi '+userobj.username + \
            ' Use the link below to verify your email \n' + absurl +'\n'+"username = "+ userobj.email+'\n'+"password = "+passwordobj
            data = {'email_body': email_body, 'to_email': userobj.username,'email_subject': 'Verify your email',
                    "username": userobj.email, "password":passwordobj}
            Util.send_email(data)
            return redirect('BoosMarketingAddAdmin')

class ProfileInDetails(View):
    def get(self, request, id):
        propertyobj = None
        propertyobj1 = None
        propertyobj2 = None
        propertyobj3 = None
        user, usertype, userprofile = get_user_usertype_userprofile(request, id)
        if userprofile:
            # userprofileobj=UserProfile.objects.get(id=id)
            
            if userprofile.user_type.user_type==1:
                propertyobj = Guest_Users_Save_Listing.objects.filter(user = userprofile.user_type.user.id) # Save Property
                propertyobj1 = Seen_Property_listing.objects.filter(user_profile_id = userprofile.user_type.user.id) # Seen Property
                propertyobj2 = None
                propertyobj3 = None
            elif userprofile.user_type.user_type==2:
                propertyobj = Property_Detail.objects.filter(user_profile = userprofile.id, is_property_open=True) # Open listing
                propertyobj1 = Property_Detail.objects.filter(user_profile = userprofile.id, is_property_open=False) # Close listing
                propertyobj2 = Property_Detail.objects.filter(user_profile = userprofile.id, is_property_expired=False) # current listing
                propertyobj3 = Property_Detail.objects.filter(user_profile = userprofile.id, is_property_expired=True) # expire listing
            else:
                propertyobj = None
                propertyobj1 = None
                propertyobj2 = None
                propertyobj3 = None
            context={"userprofileobj":userprofile,'propertyobj':propertyobj,'propertyobj1':propertyobj1,"propertyobj2":propertyobj2,"propertyobj3":propertyobj3}
            return render(request,"NewTemplate/ProfileDetail.html",context)
        else:
            messages.error(request, f"Proile Not Found")
            return redirect('AllProfileDashboard')

from django.http import JsonResponse
import requests

class AdminBasicPage(View):
    def get(self, request):
        return render(request,"NewTemplate/AdminBasic.html")

class Api_AllUser(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/AllTypeUser/?search={search_query}')
        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)

class Api_GuestUser(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/GuestTypeUser/?search={search_query}')
        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)

class Api_AgentUser(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/AgentTypeUser/?search={search_query}')
        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)

class Api_InvestorUser(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/InvestorAndDeveloperUser/?search={search_query}')
        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)

class Api_FsbhoUser(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/FsbhoAndFrbhoUser/?search={search_query}')
        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)

class Api_ManagementUser(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/ManagementUser/?search={search_query}')
        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)

class Api_SubAgentUser(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/SubAgentUser/?search={search_query}')
        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)

class Api_BoostMarketingUser(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/BoostMarketingUser/?search={search_query}')
        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)

class Api_AdvertisementUser(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/AdvertisementUserList/?search={search_query}')
        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)

class Api_InactiveUser(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/InactiveUserList/?search={search_query}')
        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)

class API_Country(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/CountryAdminAPI/?search={search_query}')
        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)

class API_State(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/StateAdminAPI/?search={search_query}')
        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)

class API_City(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/CityAdminAPI/?search={search_query}')
        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)

class API_Area(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/AreaAdminAPI/?search={search_query}')
        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)

class API_ZipCode(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/ZipCodeAdminAPI/?search={search_query}')
        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)

class API_Neighborhood(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/AllNBSpecilityAdminAPI/?search={search_query}')
        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)

class API_AgentLic(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/AllPendingLicenceAdminAPI/?search={search_query}')
        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)

class API_AllSupportList(View):
    def get(self, request, format=None):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/AllSupportTicketAdminAPI/?search={search_query}')
        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)

class API_AgentSupportList(View):
    def get(self, request, format=None):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/AllAgentSupportTicketAdminAPI/?search={search_query}')
        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)

class API_GuestSupportList(View):
    def get(self, request, format=None):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/AllGuestSupportTicketAdminAPI/?search={search_query}')
        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)
    
class API_LanguageList(View):
    def get(self, request, format=None):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/AllLanguageAdminAPI/?search={search_query}')
        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)

class API_TermsList(View):
    def get(self, request, format=None):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/TermsAdminAPI/?search={search_query}')
        
        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)

class API_OfferList(View):
    def get(self, request, format=None):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/OfferAdminAPI/?search={search_query}')
        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)

class API_HomeCardList(View):
    def get(self, request, format=None):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/HomeCardAdminAPI/?search={search_query}')

        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)


class PropertyListingAdminShow(View):
    def get(self, request, format=None):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/PropertyListingAdminAPI/?search={search_query}')

        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)

class PropertyListingTypeAdminShow(View):
    def get(self, request, format=None):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/PropertyTypeListingAdminAPI/?search={search_query}')

        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)

class PropertyMainCategoryAdminShow(View):
    def get(self, request, format=None):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/MainCategoryAdminAPI/?search={search_query}')

        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)

class PropertySubCategoryAdminShow(View):
    def get(self, request, format=None):
        search_query = request.GET.get('search', '')
        current_site = get_current_site(request).domain
        response = requests.get(f'http://{current_site}/api/admin/Property_Sub_CategoryAdminAPI/?search={search_query}')

        data = response.json()
        paginator = Paginator(data['data'], 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        paginated_data = page_obj.object_list
        response_data = {
            'results': paginated_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_number': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(response_data)


class AdminHomeCardTitle(View):
    def post(self, request):
        Title=request.POST.get('Title')
        Subtitle=request.POST.get('Subtitle')
        HomeCardTitle.objects.create(Title=Title, Subtitle=Subtitle)
        return redirect('/Toolspage') 

class AdminHomeCardAdd(View):
    def post(self, request):
        Icon=request.FILES.get('Icon')
        Card_Title=request.POST.get('Card_Title')
        Card_Body=request.POST.get('Card_Body')
        obj=HomeCard.objects.create(Icon=Icon, Card_Title=Card_Title, Card_body=Card_Body)
        return redirect('/Toolspage')

class Uploadlanguage(View):
    def post(self, request):
        dataset = Dataset()
        file = request.FILES['myfile']
        imported_data = dataset.load(file.read(),format='xlsx')
        for data in imported_data:
            value = LanguageMaster.objects.create(languages_name=data[0],position=data[1]) 
        return redirect('/Toolspage')

class LanguageMasterView(View):
    def post(self, request):
        language_name=request.POST.get('language_name')
        position=request.POST.get('position')
        try:
            LanguageMaster.objects.create(languages_name=language_name,position=position)
        except:
            # print("Already added")
            pass
        return redirect('/Toolspage')

# class DeleteLanguageMasterView(View):
#     def get(self, request,id):
#         # print(id)
#         # languagemasterobj=LanguageMaster.objects.get(id=id)
#         # languagemasterobj.delete()
#         return redirect('Toolspage')

class Deletelanguage(View):
    def get(self, request, id):
        languagemasterobj=LanguageMaster.objects.get(id=id)
        languagemasterobj.delete()
        return redirect("/Toolspage")

class DeleteTerms(View):
    def get(self, request, id):
        termsmasterobj=Terms.objects.get(id=id)
        termsmasterobj.delete()
        return redirect("/Toolspage")

class DeleteOffer(View):
    def get(self, request, id):
        Offermasterobj=Offer.objects.get(id=id)
        Offermasterobj.delete()
        return redirect("/Toolspage")

class HomeCardDelete(View):
    def get(self, request,id):
        homecardobj=HomeCard.objects.get(id=id)
        homecardobj.delete()
        return redirect('/Toolspage')

class HomeCardTitleDelete(View):
    @method_decorator(login_required(login_url='/adminlogin'))
    def get(self, request,id):
        homecardtitleobj=HomeCardTitle.objects.get(id=id)
        homecardtitleobj.delete()
        return redirect('/Toolspage')
    
class AdminCountryMasterDelete(View):
    @method_decorator(login_required(login_url='/adminlogin'))    
    def get(self, request,id):
       countrymasterobj=CountryMaster.objects.get(id=id) 
       countrymasterobj.delete()
       return redirect('/GeoDataBasePage')

class AddCountryAdmin(View):
    def post(self, request):
        position=request.POST.get("position")
        country_code=request.POST.get('country_code')
        country_name=request.POST.get('country_name')
        if CountryMaster.objects.filter(country_code=country_code) and CountryMaster.objects.filter(country_name=country_name):
            # print("Please do Unique Entry")
            pass
        else:
            CountryMaster.objects.create(position=position, country_code=country_code, country_name=country_name)
        return redirect('/GeoDataBasePage')
    
    def get(self, request, id):
        countryobj = CountryMaster.objects.get(id=id).delete()
        return redirect('/GeoDataBasePage')

class AddStateAdmin(View):
    def post(self, request):
        country_id=request.POST.get('country_id')
        countryobj=CountryMaster.objects.get(id=country_id)
        state_name=request.POST.get('state_name')
        position=request.POST.get('position')
        StateMaster.objects.create(country_master=countryobj,state_name=state_name,position=position)
        return redirect('/GeoDataBasePage')
    
    def get(self, request, id):
        stateobj = StateMaster.objects.get(id=id).delete()
        return redirect('/GeoDataBasePage')

class AddCityAdmin(View):
    def post(self, request):
        state_id=request.POST.get('state_id')
        statobj=StateMaster.objects.get(id=state_id)
        image=request.FILES.get('city')
        city_name=request.POST.get('city_name')
        position=request.POST.get('position')
        CityMaster.objects.create(state_master=statobj,city_image=image,city_name=city_name,position=position)
        return redirect('/GeoDataBasePage')
    
    def get(self, request, id):
        cityobj = CityMaster.objects.get(id=id).delete()
        return redirect('/GeoDataBasePage')

class AddAreaAdmin(View):
    def post(self, request):
        area_master=request.POST.get('city_master')
        city_master=CityMaster.objects.get(id=area_master)
        area_name=request.POST.get('area_name')
        position=request.POST.get('position')
        AreaMaster.objects.create(city_master=city_master, area_name=area_name, position=position )
        return redirect('/GeoDataBasePage')  

    def get(self, request, id):
        areaobj = AreaMaster.objects.get(id=id).delete()
        return redirect('/GeoDataBasePage')  

class AddZipAdmin(View):
    def post(self, request):
        zipcode_master=request.POST.get('area_master')
        area_master=AreaMaster.objects.get(id=zipcode_master)
        zip_code=request.POST.get('zip_code')
        position=request.POST.get('position')
        ZipCodeMaster.objects.create(area_master=area_master,Zipcode=zip_code,position=position)
        return redirect('/GeoDataBasePage')
    
    def get(self, request, id):
        zipobj = ZipCodeMaster.objects.get(id=id).delete()
        return redirect('/GeoDataBasePage')

class AdminApprovedAgentNbSpeciality(View):
    def get(self, request, id):
        neighborhood = Nb_specality_area.objects.get(id =id)
        neighborhood.is_requested = False
        neighborhood.is_verified = "Approve"
        neighborhood.save()
        return redirect("ProfilePage")

class AdminRejectedAgentNbSpeciality(View):
    def get(self, request, id):
        neighborhood = Nb_specality_area.objects.get(id =id)
        neighborhood.is_requested = False
        neighborhood.is_verified = "Reject"
        neighborhood.save()
        return redirect("ProfilePage")
    
class AdminApprovedAgentLic(View):
    def get(self, request, id):
        agentlicobj=AgentLic.objects.get(id=id)
        agentlicobj.is_validated=True
        agentlicobj.lic_already_use=True
        agentlicobj.is_requested=False
        agentlicobj.is_rejected=False
        agentlicobj.save()
        UserTypeobj=UserType.objects.get(user=agentlicobj.user.id)
        userprofileobj=UserProfile.objects.get(user_type=UserTypeobj)
        userprofileobj.brokerage_name=agentlicobj.Full_name
        userprofileobj.sales_persones_license=agentlicobj.license_number
        userprofileobj.agent_broker_license_title=agentlicobj.lic_Type
        userprofileobj.save()
        agentobj = AgentApprovedSubscriptionPlan.objects.filter(user= agentlicobj.user)
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
        return redirect("ProfilePage")

class AdminRejectAgentLic(View):
    def get(self, request, id):
        agentlicobj=AgentLic.objects.get(id=id)
        agentlicobj.is_rejected=True
        agentlicobj.is_validated=False
        agentlicobj.lic_already_use=False
        agentlicobj.is_requested=True
        agentlicobj.user=None
        agentlicobj.save()
        return redirect("ProfilePage")

class AdminBlockUser(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request, pk):
        requestpage = request.GET.get('requestpath')
        userobj=User.objects.get(id=pk)
        userobj.is_active=False
        userobj.save()
        if requestpage:
            return redirect(f"/ProfileInDetails/{pk}")
        else:
            return redirect("/ProfilePage")

class AdminUnBlockUser(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request, pk):
        requestpage = request.GET.get('requestpath')
        userobj=User.objects.get(id=pk)
        userobj.is_active=True
        userobj.save()
        if requestpage:
            return redirect(f"/ProfileInDetails/{pk}")
        else:
            return redirect("/ProfilePage")

class AdminSuspendUser(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request, pk):
        requestpage = request.GET.get('requestpath')
        userobj=User.objects.get(id=pk)
        userobj.is_suspended=True
        userobj.save()
        if requestpage:
            return redirect(f"/ProfileInDetails/{pk}")
        else:
            return redirect("/ProfilePage")

class AdminUnSuspendUser(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request, pk):
        requestpage = request.GET.get('requestpath')
        userobj=User.objects.get(id=pk)
        userobj.is_suspended=False
        userobj.save()
        if requestpage:
            return redirect(f"/ProfileInDetails/{pk}")
        else:
            return redirect("/ProfilePage")

class UpdateCountryDataAdmin(View):
    def post(self, request, id):
        countrymasterobj=CountryMaster.objects.get(id=id)
        position=request.POST.get('position')
        country_code=request.POST.get('country_code')
        country_name=request.POST.get('country_name')
        is_active=request.POST.get('is_active')

        countrymasterobj.country_code = country_code
        countrymasterobj.country_name = country_name
        countrymasterobj.is_active = is_active
        countrymasterobj.position = position

        countrymasterobj.save()
        return redirect('/GeoDataBasePage')

class UploadPropertyDataAdmin(View):
    def post(self, request):
        dataset = Dataset()
        file = request.FILES.get('myfileproperty')
        import_data = dataset.load(file.read(), format = 'xlsx')
        for i in import_data:
            if Propertylisting_type.objects.filter(property_listing_name = i[0]).exists():
                listing_obj = Propertylisting_type.objects.get(property_listing_name = i[0])
            else:
                listing_obj = Propertylisting_type.objects.create(property_listing_name = i[0], position = i[1])
            
            if Property_Listing_Type.objects.filter(listing_type = i[2]).exists():
                listingobj1 = Property_Listing_Type.objects.get(listing_type = i[2])
            else:
                listingobj1 = Property_Listing_Type.objects.create(type_of_listing = listing_obj,listing_type = i[2], user_listing_type = i[3], listing_position = i[4])
            
            # mainobj = Property_Main_Category.objects.create(listing_type = listingobj1,Main_category = i[5], category_position = i[6])

            if Property_Main_Category.objects.filter(listing_type = listingobj1,Main_category = i[5]).exists():
                mainobj = Property_Main_Category.objects.filter(listing_type = listingobj1).get(Main_category = i[5])
            else:
                mainobj = Property_Main_Category.objects.create(listing_type = listingobj1,Main_category = i[5], category_position = i[6])
            
            if i[7] != None:
                Property_Sub_Category.objects.create(property_main_category = mainobj, category_position = i[8], property_sub_category_Name = i[7])
            else:
                pass
        return redirect("/GeoDataBasePage")
    
class PropertyMainlistingDelete(View):
    def get(self, request, id):
        propertyobj = Propertylisting_type.objects.get(id=id).delete()
        return redirect("/GeoDataBasePage")
    
class PropertySublistingDelete(View):
    def get(self, request, id):
        propertyobj = Property_Listing_Type.objects.get(id=id).delete()
        return redirect("/GeoDataBasePage")
    
class PropertyMainCategoryDelete(View):
    def get(self, request, id):
        propertyobj = Property_Main_Category.objects.get(id=id).delete()
        return redirect("/GeoDataBasePage")
    
class PropertySubCategoryDelete(View):
    def get(self, request, id):
        propertyobj = Property_Sub_Category.objects.get(id=id).delete()
        return redirect("/GeoDataBasePage")

class UpdateLanguageAdmin(View):
    def post(self, request, id):
        languageobj = LanguageMaster.objects.get(id=id)
        name = request.POST.get('language_name')
        position = request.POST.get('position')
        languageobj.languages_name = name
        languageobj.position = position
        languageobj.save()
        return redirect('/Toolspage')

class UpdateHomeCardTitleAdmin(View):
    def post(self, request, id):
        hometitleobj = HomeCardTitle.objects.get(id=id)
        hometitleobj.Title=request.POST.get('Title')
        hometitleobj.Subtitle=request.POST.get('Subtitle')
        hometitleobj.save()
        return redirect('/Toolspage')

class UpdateHomeCardAdmin(View):
    def post(self, request, id):
        homecardobj = HomeCard.objects.get(id=id)
        iconobj = request.FILES.get('Icon')
        if iconobj:
            homecardobj.Icon = iconobj
        else:
            pass
        homecardobj.Card_Title = request.POST.get('Title')
        homecardobj.Card_body = request.POST.get('Subtitle')
        homecardobj.save()
        return redirect('/Toolspage')

class AddAdminMainListingType(View):
    def post(self, request, id = None):
        if id == None:
            main_listing = request.POST.get('main_listing_type')
            main_listing_postion = request.POST.get('listingposition')
            propertyobj = Propertylisting_type.objects.create(
                property_listing_name = main_listing, position = main_listing_postion
            )
        else:
            propertyobj = Propertylisting_type.objects.get(id=id)
            propertyobj.property_listing_name = request.POST.get('main_listing_type')
            propertyobj.position = request.POST.get('listingposition')
            propertyobj.save()
        return redirect("/GeoDataBasePage")

class AddAdminSubListingType(View):
    def post(self, request, id=None):
        if id == None:
            mainlistingobj = request.POST.get('listing')
            propertylistingobj = Propertylisting_type.objects.get(id = mainlistingobj)
            listing_type = request.POST.get('sub_listing_type')
            user_listing = request.POST.get('user_listing_type')
            listing_position = request.POST.get('listingposition')
            propertyobj = Property_Listing_Type.objects.create(
                type_of_listing = propertylistingobj, listing_type = listing_type, user_listing_type = user_listing, listing_position = listing_position
            )
        else:
            pass
        return redirect("/GeoDataBasePage")
    
class AddAdminMainCategory(View):
    def post(self, request, id=None):
        if id == None:
            sublistingobj = request.POST.get('sublistingtype')
            propertysubid = Property_Listing_Type.objects.get(id = sublistingobj)
            main_category_name = request.POST.get('main_category')
            main_category_position = request.POST.get('main_categoryposition')
            maincategoryobj = Property_Main_Category.objects.create(
                listing_type = propertysubid, Main_category = main_category_name, category_position = main_category_position
            )
        else:
            pass
        return redirect("/GeoDataBasePage")

class AddAdminSubCategory(View):
    def post(self, request, id=None):
        if id == None:
            maincategoryobj = request.POST.get('main_category_id')
            maincategoryidobj = Property_Main_Category.objects.get(id = maincategoryobj)
            subcategoryname = request.POST.get('sub_category_name')
            subcategoryposition = request.POST.get('sub_categoryposition')
            subcategoryobj = Property_Sub_Category.objects.create(
                property_main_category = maincategoryidobj, category_position = subcategoryposition, property_sub_category_Name = subcategoryname
            )
        else:
            pass
        return redirect("/GeoDataBasePage")


class EditSubListingType(View):
    def get(self, request):
        propertyobj = Propertylisting_type.objects.all().values('id', 'property_listing_name')
        return HttpResponse(json.dumps(list(propertyobj)), content_type = 'application/json')

    def post(self, request, id):
        propertyobj = Property_Listing_Type.objects.get(id=id)
        propertyid = request.POST.get('listing')
        propertyobjid = Propertylisting_type.objects.get(id = propertyid)
        sub_listing = request.POST.get('sub_listing_type')
        userlisting = request.POST.get('user_listing_type')
        listing_position = request.POST.get('listingposition')
        status = request.POST.get('is_active')
        propertyobj.type_of_listing = propertyobjid
        propertyobj.listing_type = sub_listing
        propertyobj.user_listing_type = userlisting
        propertyobj.listing_position = listing_position
        if status == 1:
            propertyobj.is_active = True
        else:
            propertyobj.is_active = False
        
        propertyobj.save()
        return redirect('/GeoDataBasePage')

class EditMainCategory(View):
    def get(self, request):
        listing_id = request.GET.get('listing_id')
        propertyobjid = Propertylisting_type.objects.get(id = listing_id)
        propertyobj = Property_Listing_Type.objects.filter(type_of_listing=propertyobjid).values('id', 'listing_type')
        return HttpResponse(json.dumps(list(propertyobj)), content_type = 'application/json')

    def post(self, request, id):
        maincategoryobj = Property_Main_Category.objects.get(id = id)
        sub_listing_id = request.POST.get('sublistingname')
        propertyobj = Property_Listing_Type.objects.get(id = sub_listing_id)
        name = request.POST.get('main_category')
        position = request.POST.get('main_categoryposition')
        status = request.POST.get('is_active')

        maincategoryobj.listing_type = propertyobj
        maincategoryobj.Main_category = name
        maincategoryobj.category_position = position
        if status == 1:
            maincategoryobj.is_active = True
        else:
            maincategoryobj.is_active = False
        maincategoryobj.save()

        return redirect('/GeoDataBasePage')

class EditSubCategory(View):
    def get(self, request):
        sub_listing_id = request.GET.get('sub_id')
        sub_listing_obj = Property_Listing_Type.objects.get(id = sub_listing_id)
        main_category_obj = Property_Main_Category.objects.filter(listing_type = sub_listing_obj).values('id', 'Main_category')
        return HttpResponse(json.dumps(list(main_category_obj)), content_type = 'application/json')
    
class SalesDashboard(View):
    def get(self, request):
        return render(request, 'NewTemplate/AdminSalesDashboard.html')

class AllSublistingTypeView(View):
    def get(self, request):
        listing_id = request.GET.get('listing_id')
        propertyobjid = Propertylisting_type.objects.get(property_listing_name = listing_id)
        propertyobj = Property_Listing_Type.objects.filter(type_of_listing=propertyobjid).values('id', 'listing_type')
        return HttpResponse(json.dumps(list(propertyobj)), content_type = 'application/json')

class AllMainCategoryTypeView(View):
    def get(self, request):
        sub_listing_id = request.GET.get('sub_id')
        sub_listing_obj = Property_Listing_Type.objects.get(listing_type = sub_listing_id)
        main_category_obj = Property_Main_Category.objects.filter(listing_type = sub_listing_obj).values('id', 'Main_category')
        return HttpResponse(json.dumps(list(main_category_obj)), content_type = 'application/json')

class AllSubCategoryTypeView(View):
    def get(self, request):
        main_listing_id = request.GET.get('main_id')
        sub_listing_id = request.GET.get('sub_listing')
        sub_listing_obj = Property_Listing_Type.objects.get(listing_type = sub_listing_id)
        main_listing_sub = Property_Main_Category.objects.filter(Main_category = main_listing_id).get(listing_type = sub_listing_obj)
        sub_category_obj = Property_Sub_Category.objects.filter(property_main_category = main_listing_sub).values('id','property_sub_category_Name')
        return HttpResponse(json.dumps(list(sub_category_obj)), content_type = 'application/json')

class AddPropertylistingAll(View):
    def post(self, request):
        main_listing_id = request.POST.get('main_listing_id')
        sub_listing_id = request.POST.get('sub_listing_id')
        main_category_id = request.POST.get('main_category_id')
        main_category_position = request.POST.get('main_category_position')
        sub_category_id = request.POST.get('sub_category_id')
        sub_category_postition = request.POST.get('sub_category_postition')

        main_listing = Propertylisting_type.objects.last()
        main_listing_position = main_listing.position + 1
        if Propertylisting_type.objects.filter(property_listing_name = main_listing_id):
            propertyobjid = Propertylisting_type.objects.get(property_listing_name = main_listing_id)
        else:
            propertyobjid = Propertylisting_type.objects.create(property_listing_name = main_listing_id, position = main_listing_position)
        
        sub_listing = Property_Listing_Type.objects.filter(type_of_listing=propertyobjid).last()
        if sub_listing:
            sub_listing_position = int(sub_listing.listing_position) + 1
        else:
            sub_listing_position = 1

        if Property_Listing_Type.objects.filter(type_of_listing = propertyobjid,listing_type = sub_listing_id):
            sub_listing_obj = Property_Listing_Type.objects.get(listing_type = sub_listing_id)
        else:
            sub_listing_obj = Property_Listing_Type.objects.create(type_of_listing = propertyobjid,listing_type = sub_listing_id, listing_position = sub_listing_position)
        
        if Property_Main_Category.objects.filter(listing_type = sub_listing_obj, Main_category = main_category_id):
            main_category_obj = Property_Main_Category.objects.filter(Main_category = main_category_id).get(listing_type = sub_listing_obj)
        else:
            main_category_obj = Property_Main_Category.objects.create(Main_category = main_category_id,listing_type = sub_listing_obj, category_position = main_category_position)
        
        if Property_Sub_Category.objects.filter(property_main_category = main_category_obj, property_sub_category_Name = sub_category_id):
            sub_category_obj = Property_Sub_Category.objects.filter(property_sub_category_Name = sub_category_id).get(property_main_category = main_category_obj)
        else:
            sub_category_obj = Property_Sub_Category.objects.create(property_sub_category_Name = sub_category_id, property_main_category = main_category_obj, category_position = sub_category_postition)
        return redirect('/GeoDataBasePage')

class AdminAddBoostMarketingUser(View):
    def post(self, request):
        # print(request.POST)
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        password = request.POST.get('password')
        # password = secrets.token_hex(16)
        encrypted_string = encrypt(key, password)

        work_number=request.POST.get('work_number')
        short_description=request.POST.get('short_description')
        select_service=request.POST.getlist('select_service')
        profile=request.FILES.get('profile')

        if User.objects.filter(username=email):
            pass
        else:
            userobj=User.objects.create(email=email, username=email, password=encrypted_string,is_active=True)
            # print('user : ', userobj)
            usertype=UserType.objects.create(user=userobj,user_type=7)
            # print('user type : ', usertype)
            UserProfile.objects.create(user_type=usertype,first_name=first_name,last_name=last_name,work_number_1=work_number,personal_bio=short_description,unique_id='boost',profile_image=profile)
            for item in select_service:
                BoostMarketingServicesTOUser.objects.create(user=userobj, ServiceNumber=item)
            
            passwordobj = decrypt(key, userobj.password)
            current_site = get_current_site(request).domain
            absurl = 'http://'+current_site+'/Boost-Marketing-Admin-Login/'
            email_body = 'Hi '+userobj.username + \
            ' Use the link below to verify your email \n' + absurl +'\n'+"username = "+ userobj.email+'\n'+"password = "+passwordobj
            data = {'email_body': email_body, 'to_email': userobj.username,'email_subject': 'Verify your email',
                    "username": userobj.email, "password":passwordobj}
            Util.send_email(data)
        return redirect("/ProfilePage")

class AdminSecurityandPassword(View):
    def get(self, request):
        return render(request, 'NewTemplate/AdminSecurity&password.html', {'user_id': request.user.id})

    def post(self, request):
        user_id = request.POST.get('userid')
        if User.objects.filter(id=user_id):
            user = User.objects.get(id=user_id)
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            user_object=authenticate(username=user.username,password=old_password)
            if user_object is not None:
                if new_password == confirm_password:
                    user_object.set_password(new_password)
                    user_object.save()
                    logout(request)
                    return redirect('/')
                else:
                    return redirect('/AdminSecurityandPassword')
            else:
                return redirect('/AdminSecurityandPassword')
        else:
            return redirect('/AdminSecurityandPassword')

class AllStateDataName(View):
    def get(self, request):
        country_name = request.GET.get('Country_name')
        country_id = CountryMaster.objects.get(country_name = country_name)
        state_data = StateMaster.objects.filter(country_master = country_id).values('id','state_name')
        return HttpResponse(json.dumps(list(state_data)), content_type = 'application/json')
    
class AllCityDataName(View):
    def get(self, request):
        state_name = request.GET.get('state_name')
        state_id = StateMaster.objects.get(state_name = state_name)
        city_data = CityMaster.objects.filter(state_master = state_id).values('id','city_name')
        return HttpResponse(json.dumps(list(city_data)), content_type = 'application/json')
    
class AllTownDataName(View):
    def get(self, request):
        city_name = request.GET.get('city_name')
        city_id = CityMaster.objects.get(city_name = city_name)
        area_data = AreaMaster.objects.filter(city_master = city_id).values('id','area_name')
        return HttpResponse(json.dumps(list(area_data)), content_type = 'application/json')
    
class AllZipCodeDataName(View):
    def get(self, request):
        area_name = request.GET.get('area_name')
        area_id = AreaMaster.objects.get(area_name = area_name)
        zip_data = ZipCodeMaster.objects.filter(area_master = area_id).values('id','Zipcode')
        return HttpResponse(json.dumps(list(zip_data)), content_type = 'application/json')

class LocationAddAdminSide(View):
    def post(self, request):
        country_name = request.POST.get('country_name')
        country_code = request.POST.get('country_code')
        state_name = request.POST.get('state_name')
        city_name = request.POST.get('city_name')
        city_position = request.POST.get('cityposition_name')
        area_name = request.POST.get('town_name')
        area_position = request.POST.get('townposition_name')
        zip_code = request.POST.get('zip_name')
        zip_code_position = request.POST.get('zipposition_name')

        country_listing = CountryMaster.objects.last()
        country_position = country_listing.position + 1
        if country_name:
            if CountryMaster.objects.filter(country_name = country_name):
                countryobj = CountryMaster.objects.get(country_name = country_name)
            else:
                countryobj = CountryMaster.objects.create(country_name = country_name, country_code = country_code, position = country_position)
        
        state_listing = StateMaster.objects.filter(country_master = countryobj).last()
        state_position = state_listing.position + 1
        if state_name:
            if StateMaster.objects.filter(state_name = state_name):
                stateobj = StateMaster.objects.get(state_name = state_name)
            else:
                stateobj = StateMaster.objects.create(country_master = countryobj, position = state_position, state_name = state_name)

        if city_name:
            if CityMaster.objects.filter(state_master = stateobj, city_name = city_name):
                cityobj = CityMaster.objects.filter(state_master = stateobj).get(city_name = city_name)
            else:
                cityobj = CityMaster.objects.create(state_master = stateobj, city_name = city_name, position = city_position)
        
        if area_name:
            if AreaMaster.objects.filter(city_master = cityobj, area_name = area_name):
                areaobj = AreaMaster.objects.filter(city_master = cityobj).get(area_name = area_name)
            else:
                areaobj = AreaMaster.objects.create(city_master = cityobj, area_name = area_name, position = area_position)
        
        if zip_code:
            if ZipCodeMaster.objects.filter(area_master = areaobj, Zipcode = zip_code):
                zipobj = ZipCodeMaster.objects.filter(area_master = areaobj).get(Zipcode = zip_code)
            else:
                zipobj = ZipCodeMaster.objects.create(area_master = areaobj, Zipcode = zip_code, position = zip_code_position)

        return redirect('/GeoDataBasePage')

class ApproveSupportRequest(View):
    def get(self, request, id=None):
        support = SupportTickets.objects.get(id = id)
        support.status = True
        support.is_request = False
        support.save()
        return redirect("/AdminDashboard")
    
class RejectSupportRequest(View):
    def get(self, request, id=None):
        support = SupportTickets.objects.get(id = id)
        support.status = False
        support.is_request = False
        support.save()
        return redirect("/AdminDashboard")