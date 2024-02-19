from property.models import *
from .models import *
from django.shortcuts import render, redirect
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
from accounts.models import User, UserType, UserProfile
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

class CountryMasterView(View):
    @method_decorator(login_required(login_url='/adminlogin'))
    def get(self, request):
        # search
          if 'q' in request.GET:
              q=request.GET['q']
              multiple_q=Q(Q(country_name__icontains=q) | Q(country_code__icontains=q))
              CountryMaster_obj=CountryMaster.objects.filter(multiple_q)
          else:
              CountryMaster_obj=CountryMaster.objects.all()
          # paginator
          paginator=Paginator(CountryMaster_obj,20)
          page_number=request.GET.get('page')
          CountryMaster_obj=paginator.get_page(page_number)
          obj=paginator.page_range
        
          context={"CountryMaster_obj":CountryMaster_obj, "obj":obj }
          return render(request,'CountryMaster.html',context)
              

    def post(self, request):
        position=request.POST.get("position")
        country_code=request.POST.get('country_code')
        country_name=request.POST.get('country_name')

        if CountryMaster.objects.filter(country_code=country_code) and CountryMaster.objects.filter(country_name=country_name):
            # print("Please do Unique Entry")
            pass
        else:
            CountryMaster.objects.create(position=position, country_code=country_code, country_name=country_name)

        return redirect('/countrymasterview')    

class CountryMasterEdit(View):
    @method_decorator(login_required(login_url='/adminlogin'))
    def get(self, request,id):
        countrymasterobj=CountryMaster.objects.get(id=id)
        context={'countrymasterobj':countrymasterobj}
        return render(request,'countrymasteredit.html',context)

    def post(self, request,id):
        countrymasterobj=CountryMaster.objects.get(id=id)
        position=request.POST.get('position')
        country_code=request.POST.get('country_code')
        country_name=request.POST.get('country_name')
        is_active=request.POST.get('is_active')
        if position:
            countrymasterobj.position=position
        if country_code:
            countrymasterobj.country_code=country_code
        if country_name:
            countrymasterobj.country_name=country_name
        if is_active:
            countrymasterobj.is_active=is_active   

        countrymasterobj.save()
        return redirect('/countrymasterview')

class CountryMasterDelete(View):
    @method_decorator(login_required(login_url='/adminlogin'))    
    def get(self, request,id):
       countrymasterobj=CountryMaster.objects.get(id=id) 
       countrymasterobj.delete()
       return redirect('/countrymasterview') 

from itertools import chain
class AreaMasterView(View):
    @method_decorator(login_required(login_url='/adminlogin'))
    def get(self, request):
        citymasterobj=CityMaster.objects.filter(is_active=True)
         # search
        if 'q' in request.GET:
            q=request.GET['q']
            multiple_q=Q(Q(area_name__icontains=q)) 
            multiple_p=Q(Q(city_name__icontains=q))
            
            citymasterobj=CityMaster.objects.filter(multiple_p).values_list('id', flat=True)
            areamasterobj_city=AreaMaster.objects.filter(city_master__in=citymasterobj)
            areamasterobj_name=AreaMaster.objects.filter(multiple_q)

            result_list = list(chain(areamasterobj_city, areamasterobj_name))
        else:    
            result_list=AreaMaster.objects.all()
        # paginator
        paginator=Paginator(result_list,10)
        page_number=request.GET.get('page')
        result_list=paginator.get_page(page_number)
        obj=paginator.page_range
        context={'result_list':result_list, 'citymasterobj':citymasterobj, "obj":obj}
        return render(request, 'AreaMaster.html', context)    

    def post(self, request):
        area_master=request.POST.get('city_master')
        city_master=CityMaster.objects.get(id=area_master)
        area_name=request.POST.get('area_name')
        position=request.POST.get('position')
        AreaMaster.objects.create(city_master=city_master, area_name=area_name, position=position )
        return redirect('/areamasterview')   

class EditAreaMaster(View):
    @method_decorator(login_required(login_url='/adminlogin'))   
    def get(self, request,id):
        editareamasterobj=AreaMaster.objects.get(id=id)
        editcitymasterobj=CityMaster.objects.filter(is_active=True)
        context={'editareamasterobj':editareamasterobj, 'editcitymasterobj':editcitymasterobj}
        return render(request,'edit-areamaster.html', context )

    def post(self, request,id):
        areamasterobj=AreaMaster.objects.get(id=id)
        area_name=request.POST.get('area_name')
        city_master=request.POST.get('city_master')
        is_active=request.POST.get('is_active')
        position=request.POST.get('position')

        if area_name:
            areamasterobj.area_name=area_name
        if city_master:
            citymasterobjcet=CityMaster.objects.get(id=city_master)
            areamasterobj.city_master=citymasterobjcet 
        if  is_active:
            areamasterobj.is_active=is_active
        if position:
            areamasterobj.position=position

        areamasterobj.save()   
        return redirect('/areamasterview')    

class DeleteAreaMaster(View):
    @method_decorator(login_required(login_url='/adminlogin'))
    def get(self, request,id):
        areamasterobj=AreaMaster.objects.get(id=id)
        areamasterobj.delete()
        return redirect('/areamasterview') 

class CouponAndPromoView(View):
    @method_decorator(login_required(login_url='/adminlogin'))
    def get(self, request):
         # search
          if 'q' in request.GET:
              q=request.GET['q']
              multiple_q=Q(Q(name__icontains=q) | Q(couponcode__icontains=q) |Q(startdate__icontains=q)|Q(enddate__icontains=q)|Q(couponfor__icontains=q))
              couponandpromoviewobj=CouponAndPromo.objects.filter(multiple_q)
          else:
              couponandpromoviewobj=CouponAndPromo.objects.all()
          # paginator
          paginator=Paginator(couponandpromoviewobj,20)
          page_number=request.GET.get('page')
          couponandpromoviewobj=paginator.get_page(page_number)
          obj=paginator.page_range   

          context={'couponandpromoviewobj':couponandpromoviewobj, "obj":obj}
          return render(request, 'manage-coupon.html',context)

    def post(self, request):
        coupon_name=request.POST.get('coupon_name')
        coupon_code=request.POST.get('coupon_code')
        account_type=request.POST.getlist('account_type')
        select_all=request.POST.get('select_all')
        start_date=request.POST.get('start_date')
        end_date=request.POST.get('end_date')
        coupon_for=request.POST.get('coupon_for')
        number_of_user=request.POST.get('number_of_user')
        user_type=request.POST.get('user_type')
        discount_type=request.POST.get('discount_type')
        discount=request.POST.get('discount')
        if select_all == None:
            CouponAndPromo.objects.create(name=coupon_name, couponcode=coupon_code, account_type=account_type, startdate=start_date, enddate=end_date, couponfor=coupon_for, number_of_user=number_of_user, user_type=user_type, discount_type=discount_type, discount=discount )
        else:
            CouponAndPromo.objects.create(name=coupon_name, couponcode=coupon_code, account_type=['1','2','3','4'], startdate=start_date, enddate=end_date, couponfor=coupon_for, number_of_user=number_of_user, user_type=user_type, discount_type=discount_type, discount=discount  )
        return redirect('/couponandpromoview')   

class EditCouponAndPromo(View):
    @method_decorator(login_required(login_url='/adminlogin'))
    def get(self, request,id):
        editcouponandpromo=CouponAndPromo.objects.get(id=id)
        context={'editcouponandpromo':editcouponandpromo}
        return render(request, 'edit-couponandpromo.html',context)

    def post(self, request,id):
        editcouponandpromo=CouponAndPromo.objects.get(id=id)
        coupon_name=request.POST.get('coupon_name')
        coupon_code=request.POST.get('coupon_code')
        account_type=request.POST.getlist('account_type')
        select_all=request.POST.get('select_all')
        start_date=request.POST.get('start_date')
        end_date=request.POST.get('end_date')
        coupon_for=request.POST.get('coupon_for')
        number_of_user=request.POST.get('number_of_user')
        user_type=request.POST.get('user_type')
        discount_type=request.POST.get('discount_type')
        discount=request.POST.get('discount')
        is_active=request.POST.get('is_active')
    
        if coupon_name:
            editcouponandpromo.name=coupon_name
        if coupon_code:
            editcouponandpromo.couponcode=coupon_code
        
        if select_all == None:
            if account_type:
                editcouponandpromo.account_type=account_type 
        else:
            editcouponandpromo.account_type=["1","2","3","4"]
           
          
           
        if start_date:
            editcouponandpromo.startdate=start_date 
        if end_date:
            editcouponandpromo.enddate=end_date
        if coupon_for:
            editcouponandpromo.couponfor=coupon_for
        if number_of_user:
            editcouponandpromo.number_of_user=number_of_user  
        if user_type:
            editcouponandpromo.user_type=user_type
        if discount_type:
            editcouponandpromo.discount_type=discount_type
        if discount:
            editcouponandpromo.discount=discount
        if is_active:
            editcouponandpromo.is_active=is_active  
        editcouponandpromo.save()          
        return redirect('/couponandpromoview')    

class DeleteCouponAndPromo(View):
    @method_decorator(login_required(login_url='/adminlogin'))
    def get(self, request,id):
        couponandpromoviewobj=CouponAndPromo.objects.get(id=id)
        couponandpromoviewobj.delete()
        return redirect('/couponandpromoview') 

# Zip code Master
class ZipCodeMasterView(View):
    @method_decorator(login_required(login_url='/adminlogin'))
    def get(self, request):
        areamasterobj=AreaMaster.objects.filter(is_active=True)
        # Search
        if 'q' in request.GET:
            q = request.GET['q']
            multiple_q=Q(Q(Zipcode__icontains=q))
            multiple_p=Q(Q(area_name__icontains=q))

            areamasterobj = AreaMaster.objects.filter(multiple_p).values_list('id', flat=True)
            zipcodemasterobj_area = ZipCodeMaster.objects.filter(area_master__in=areamasterobj)
            zipcodemasterobj_name = ZipCodeMaster.objects.filter(multiple_q)

            result_list = list(chain(zipcodemasterobj_area, zipcodemasterobj_name))
        else:
            result_list = ZipCodeMaster.objects.all()
        
        # paginator
        paginator = Paginator(result_list, 10)
        page_number = request.GET.get('page')
        result_list = paginator.get_page(page_number)
        obj = paginator.page_range
        context={'result_list':result_list, 'areamasterobj':areamasterobj, "obj":obj}
        return render(request, 'ZipCodeMaster.html', context)
    
    def post(self, request):
        zipcode_master=request.POST.get('area_master')
        area_master=AreaMaster.objects.get(id=zipcode_master)
        zip_code=request.POST.get('zip_code')
        position=request.POST.get('position')
        ZipCodeMaster.objects.create(area_master=area_master,Zipcode=zip_code,position=position)
        return redirect('/zipcodemasterview')

class EditZipCodeMaster(View):
    @method_decorator(login_required(login_url='/adminlogin'))
    def get(self, request, id):
        editzipcodemasterobj=ZipCodeMaster.objects.get(id=id)
        editareamasterobj=AreaMaster.objects.filter(is_active=True)
        context={'editzipcodemasterobj':editzipcodemasterobj,'editareamasterobj':editareamasterobj}
        return render(request,'edit-zipcodemaster.html', context)
    
    def post(self, request, id):
        zipcodemasterobj=ZipCodeMaster.objects.get(id=id)
        zip_code=request.POST.get('zip_code')
        area_master=request.POST.get('area_master')
        is_active=request.POST.get('is_active')
        position=request.POST.get('position')

        if zip_code:
            zipcodemasterobj.Zipcode=zip_code
        if area_master:
            areamasterobject=AreaMaster.objects.get(id=area_master)
            zipcodemasterobj.area_master=areamasterobject
        if is_active:
            zipcodemasterobj.is_active=is_active
        if position:
            zipcodemasterobj.position=position
        
        zipcodemasterobj.save()
        return redirect('/zipcodemasterview')
    
class DeleteZipCodeMaster(View):
    @method_decorator(login_required(login_url='/adminlogin'))
    def get(self, request, id):
        zipcodemasterobj=ZipCodeMaster.objects.get(id=id)
        zipcodemasterobj.delete()
        return redirect('/zipcodemasterview')

# Pet Master
class PetMasterView(View):
    @method_decorator(login_required(login_url='/adminlogin'))
    def get(self, request):
        # serach
        if 'q' in request.GET:
            q=request.GET['q']
            multiple_q=Q(Q(Pet_Name__icontains=q))
            petmasterobj=PetMaster.objects.filter(multiple_q)
        else:
            petmasterobj=PetMaster.objects.all()

        # paginator
        paginator=Paginator(petmasterobj,20)
        page_number=request.GET.get('page')
        petmasterobj=paginator.get_page(page_number)
        obj=paginator.page_range

        context={"petmasterobj":petmasterobj, "obj":obj}
        return render(request, 'PetMaster.html',context)
    
    def post(self, request):
        pet_image=request.FILES.get('pet_Image')
        pet_name=request.POST.get('pet_name')
        position=request.POST.get('position')
        PetMaster.objects.create(Pet_Image=pet_image,Pet_Name=pet_name,position=position)
        return redirect('/petmasterview')

class EditPetMaster(View):
    @method_decorator(login_required(login_url='/adminlogin'))
    def get(self, request, id):
        editpetmasterobj=PetMaster.objects.get(id=id)
        context={'editpetmasterobj':editpetmasterobj}
        return render(request,'petmasteredit.html', context)
    
    def post(self, request, id):
        editpetmasterobj=PetMaster.objects.get(id=id)
        pet_image= request.FILES.get('pet_image')
        pet_name=request.POST.get('pet_name')
        position=request.POST.get('position')
        is_active=request.POST.get('is_active')

        if pet_image:
            editpetmasterobj.Pet_Image=pet_image
        if pet_name:
            editpetmasterobj.Pet_Name=pet_name    
        if position:
            editpetmasterobj.position = position
        if is_active:
            editpetmasterobj.is_active=is_active
        editpetmasterobj.save()
        return redirect("/petmasterview")
    
class DeletePetMaster(View):
    @method_decorator(login_required(login_url='/adminlogin'))
    def get(self, request, id):
        petmasterobj=PetMaster.objects.get(id=id)
        petmasterobj.delete()
        return redirect('/petmasterview')

class SearchForHome(APIView):
    def post(self, request,format=None, id=None):
        try:
            data=request.data
            if "location" in data:
                q=data['location']
                multiple_a=Q(Q(area_name__icontains=q))
                multiple_c=Q(Q(city_name__icontains=q))
                multiple_s=Q(Q(state_name__icontains=q))

                areamasterobj=AreaMaster.objects.filter(multiple_a)
                cityobj=CityMaster.objects.filter(multiple_c)
                stateobj=StateMaster.objects.filter(multiple_s)

                areaserializer=AreaSearchSerializer(areamasterobj,many=True)
                cityserializer=CitySearchSerializer(cityobj,many=True)
                stateserializer=StateSearchSerializer(stateobj,many=True)
                return Response(util.success(self,{'area':areaserializer.data, 'city':cityserializer.data, 'state':stateserializer.data}))
            else:
                return Response(util.error(self,"location is needed"))
        except Exception as e:
            return Response(util.error(self,str(e)))

# class AreaSearch(APIView):
#     def post(self, request, format=None):
#         data = request.data
#         if "area" in data:
#             q = data["area"]
#             multiple_a=Q(area_name__icontains=q)
#             areamasterobj=AreaMaster.objects.filter(multiple_a)
#             zipmasterobj = ZipCodeMaster.objects.filter(area_master__in = areamasterobj)
#             zipserializer = ZipcodeSearchSerializer(zipmasterobj, many=True)
#             if zipserializer.data:
#                 return Response(util.success(self, zipserializer.data))
#             else:
#                 return Response(util.error(self,"No Data Found"))
#         else:
#             return Response(util.error(self,'area is required'))

class AreaSearch(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
            if "location" in data:
                q=data['location']
                multiple_a=Q(Q(area_name__icontains=q))
                multiple_c=Q(Q(city_name__icontains=q))
                areamasterobj=AreaMaster.objects.filter(multiple_a)
                cityobj=CityMaster.objects.filter(multiple_c)

                # stateid=[]
                # for i in cityobj:
                #     stateid.append(i.state_master.id)
                # stateobj=StateMaster.objects.filter(id__in=stateid)
                areaserializer=AreaSearchSerializer(areamasterobj,many=True)
                # stateserializer=StateSearchSerializer(stateobj,many=True)

                # zipmasterobj = ZipCodeMaster.objects.filter(area_master__in = areamasterobj)
                # zipareaserializer=ZipcodeSearchSerializer(zipmasterobj, many=True)
                cityserializer=CitySearchSerializer(cityobj,many=True)
                return Response(util.success(self,[areaserializer.data,cityserializer.data]))
            else:
                return Response(util.error(self,'location is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class ZipSerach(APIView):
    def post(self, request, format = None):
        try:
            data = request.data
            if "zipcode" in data:
                q=data['zipcode'] ##44 4440034
                
                multiple_z=Q(Zipcode__icontains=q)
                # obj=ZipCodeMaster.objects.filter(multiple_z).distinct('Zipcode')
                # # print(obj)

                # return Response(util.success(self,"yes"))
                obj=ZipCodeMaster.objects.filter(multiple_z).values('Zipcode').distinct()
                serializer = ZipcodeSerializer(obj,many=True)
                return Response(util.success(self,serializer.data))
            else:
                return Response(util.error(self,'zipcode is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))

            
class HomeCardTitleView(View):
    @method_decorator(login_required(login_url='/adminlogin'))
    def get(self, request):
        homecardtitleobj=HomeCardTitle.objects.all()
        context={'homecardtitleobj':homecardtitleobj}
        return render(request,'HomeCardTitle.html',context)

    def post(self, request):
        Title=request.POST.get('Title')
        Subtitle=request.POST.get('Subtitle')
        HomeCardTitle.objects.create(Title=Title, Subtitle=Subtitle)
        return redirect('/homecardtitleview') 

class HomeCardTitleEdit(View):
    @method_decorator(login_required(login_url='/adminlogin'))
    def get(self, request,id):
        homecardtitleobj=HomeCardTitle.objects.get(id=id)
        context={'homecardtitleobj': homecardtitleobj}
        return render(request,'edit-homecardtitle.html',context)

    def post(self, request,id):
        homecardtitleobj=HomeCardTitle.objects.get(id=id)
        Title=request.POST.get('Title')
        Subtitle=request.POST.get('Subtitle')
        if Title:
            homecardtitleobj.Title=Title
        if Subtitle:
            homecardtitleobj.Subtitle=Subtitle
        homecardtitleobj.save()
        return redirect('/homecardtitleview')


class HomeCardView(View):
    @method_decorator(login_required(login_url='/adminlogin'))
    def get(self, request):
        #search
        if 'q' in request.GET:
            q=request.GET['q']
            multiple_q=Q(Q(Card_Title__icontains=q)  | Q(Card_body__icontains=q))
            homecardobj=HomeCard.objects.filter(multiple_q)
        else:    
            homecardobj=HomeCard.objects.all()
        #paginators
        paginator=Paginator(homecardobj,20)
        page_number=request.GET.get('page')
        homecardobj=paginator.get_page(page_number)
        obj=paginator.page_range     
        context={'homecardobj':homecardobj, "obj":obj}
        return render(request,'HomeCard.html',context)

    def post(self, request):
        Icon=request.FILES.get('Icon')
        Card_Title=request.POST.get('Card_Title')
        Card_Body=request.POST.get('Card_Body')
        obj=HomeCard.objects.create(Icon=Icon, Card_Title=Card_Title, Card_body=Card_Body)
        # print(obj)
        return redirect('/homecardview')            


class HomeCardEdit(View):
    @method_decorator(login_required(login_url='/adminlogin'))
    def get(self, request,id):
        homecardobj=HomeCard.objects.get(id=id)
        context={'homecardobj': homecardobj}
        return render(request,'edit-homecard.html',context)

    def post(self, request,id):
        homecardobj=HomeCard.objects.get(id=id)
        Icon=request.FILES.get('Icon')
        Card_Title=request.POST.get('Card_Title')
        Card_Body=request.POST.get('Card_Body')
        if Icon:
            homecardobj.Icon=Icon
        if Card_Title:
            homecardobj.Card_Title=Card_Title
        if Card_Body:
            homecardobj.Card_body=Card_Body  
        homecardobj.save()  
        return redirect('/homecardview')



class TermsAdd(View):
    @method_decorator(login_required(login_url='/adminlogin'))
    def get(self, request, id=None):
        if id is None:
            termsobj = Terms.objects.all()
            return render(request, 'terms.html',locals())
        else:
            termsobj = Terms.objects.get(id=id)
            termsobj.delete()
            return redirect('terms')
    
    def post(self, request, id = None):
        if id is None:
            terms = request.POST.get('terms')
            position = request.POST.get('position')
            termobj = Terms.objects.create(
                terms = terms, position = position
            )
            return redirect('terms')
        else:
            termsobj = Terms.objects.get(id=id)
            termsobj.terms = request.POST.get('terms')
            termsobj.position = request.POST.get('position')
            termsobj.save()
            return redirect('terms')

class AddOffers(View):
    @method_decorator(login_required(login_url='/adminlogin'))
    def get(self, request, id = None):
        if id is None:
            offersobj = Offer.objects.all()
            return render(request, 'offers.html', locals())
        else:
            offersobj = Offer.objects.get(id = id)
            offersobj.delete()
            return redirect('offers')

    def post(self, request, id = None):
        if id is None:
            offer = request.POST.get('offers')
            position = request.POST.get('position')
            offerobj = Offer.objects.create(
                offer = offer, position = position
            )
            return redirect('offers')
        else:
            offersobj = Offer.objects.get(id = id)
            offersobj.offer = request.POST.get('offers')
            offersobj.position = request.POST.get('position')
            offersobj.save()
            return redirect('offers')

class AddIssueType(View):
    @method_decorator(login_required(login_url='/adminlogin'))
    def get(self, request, id = None):
        if id is None:
            issuetypeobj = IssueType.objects.all()
            return render(request, 'issue_type.html', locals())
        else:
            issuetypeobj = IssueType.objects.get(id = id)
            issuetypeobj.delete()
            return redirect('issue_type')
    
    def post(self, request, id = None):
        if id is None:
            issues = request.POST.get('issues')
            position = request.POST.get('position')
            issuetypeobj = IssueType.objects.create(
                issue_type = issues, position = position
            )
            return redirect('issue_type')
        else:
            issuetypeobj = IssueType.objects.get(id = id)
            issuetypeobj.issue_type = request.POST.get('issues')
            issuetypeobj.position = request.POST.get('position')
            issuetypeobj.save()
            return redirect('issue_type')

class AddPriorityType(View):
    @method_decorator(login_required(login_url='/adminlogin'))
    def get(self, request, id = None):
        if id is None:
            issuepriorityobj = IssuePriority.objects.all()
            return render(request, 'priority.html', locals())
        else:
            issuepriorityobj = IssuePriority.objects.get(id = id)
            issuepriorityobj.delete()
            return redirect('issue_priority')
    
    def post(self, request, id = None):
        if id is None:
            priority = request.POST.get('priority')
            position = request.POST.get('position')
            issuepriorityobj = IssuePriority.objects.create(
                priority = priority, position = position
            )
            return redirect('issue_priority')
        else:
            issuepriorityobj = IssuePriority.objects.get(id = id)
            issuepriorityobj.priority = request.POST.get('priority')
            issuepriorityobj.position = request.POST.get('position')
            issuepriorityobj.save()
            return redirect('issue_priority')