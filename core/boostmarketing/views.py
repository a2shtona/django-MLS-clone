from django.shortcuts import render, redirect
from accounts.models import User
from django.views import View
from .serializer import *
from master import util
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from accounts.models import UserType
from . models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from django.core.paginator import Paginator
import base64
from Cryptodome.Cipher import AES

key = '01234567890123456789015545678901'

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

class BoostMarketingAdminLogin(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('/dashboard')
        return render(request, 'boostmarketingadminlogin.html')
    
    def post(self,request):
        username= request.POST['username']
        password= request.POST['password']
        user = User.objects.get(username=username)
        passwordobj = decrypt(key, user.password)
        if user is not None:
            if passwordobj==password:
                usertypeobj=UserType.objects.get(user=user)
                
                if usertypeobj.user_type==7:
                    login(request,user)
                    return redirect('/Boost-Marketing-Dashboard')
                else:
                    return redirect('/Boost-Marketing-Admin-Login')
            else:
                return redirect('/Boost-Marketing-Admin-Login') 
        else:
            return redirect('/Boost-Marketing-Admin-Login')

class BoostMarketingDashboardApi(APIView):
    def post(self,request):
        try:
            data=request.data
            if 'plan_type' in data:
                plan = Plan_Type.objects.get(plan_type = data['plan_type'])
                BoostMarkitingPlanobj=BoostMarkitingPlan.objects.filter(plan_type=data['plan_type'])
                serializer=BoostMarkitingPlanSerializer(BoostMarkitingPlanobj,many=True)
                if serializer.data:
                    return Response(util.success(self,{"description":plan.top_description,"plans":serializer.data}))
                else:
                    return Response(util.error(self,'No Data Found'))
            else:
                return Response(util.error(self,'plan_type is Needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class BoostMarketingDashboard(View):
    @method_decorator(login_required(login_url='/Boost-Marketing-Admin-Login'))
    def get(self,request):
        user = request.user
        boostservice = BoostMarketingServicesTOUser.objects.filter(user = user.id)
        context = {
            "boostservice":boostservice
        }
        return render(request, "BoostMarketingAdminDashboard.html", context)

class boostmarketingplantable(View):
    @method_decorator(login_required(login_url='/Boost-Marketing-Admin-Login'))
    def get(self, request):
        user = request.user
        boostservice = BoostMarketingServicesTOUser.objects.filter(user = user.id)
        plan = request.GET.get('plan_type')
        boostserviceid = BoostMarketingServicesTOUser.objects.filter(id=plan)
        Serviceid=[]
        for i in boostserviceid:
            Serviceid.append(i.ServiceNumber)
        boostplan = BoostMarkitingPlan.objects.filter(plan_type__in = Serviceid)
        boosttable = BoostMarketingTable.objects.filter(boostbarkitingplan__in=boostplan)

        # paginator
        paginator=Paginator(boosttable,20)
        page_number=request.GET.get('page')
        boosttable=paginator.get_page(page_number)
        obj=paginator.page_range

        context = {
            "boosttable":boosttable,"boostservice":boostservice, "obj":obj
        }
        return render(request, "BoostMarketingAdminDashboard.html", context)

class create_Boostmarketingplan(View):
    @method_decorator(login_required(login_url='/Boost-Marketing-Admin-Login'))
    def get(self, request, id=None):
        if id is None:
            boostmarketingplan=BoostMarkitingPlan.objects.all()
            context = {'boostmarketingplan':boostmarketingplan}
            return render(request, "boostmarktingplan.html", context)
        else:
            boostmarketingplan=BoostMarkitingPlan.objects.get(id=id)
            boostmarketingplan.delete()
            return redirect('/create_Boostmarketingplan')

    def post(self, request):
        plan_type = request.POST.get('plan_type')
        impression = request.POST.get('impression')
        cost = request.POST.get('cost')
        description = request.POST.get('description')
        # termsservice = request.POST.get('termandservice')
        BoostMarkitingPlanobj = BoostMarkitingPlan.objects.create(
            plan_type = plan_type, impression = impression, cost = cost, description = description
        )
        return redirect('/create_Boostmarketingplan')

class Update_BoostMarketinPlan(View):
    @method_decorator(login_required(login_url='/Boost-Marketing-Admin-Login'))
    def get(self, request, id):
        boostmarketingplan=BoostMarkitingPlan.objects.get(id=id)
        return render(request, 'edit_boostmarktingplan.html', locals())
    def post(self, request,id):
        boostmarketingplan=BoostMarkitingPlan.objects.get(id=id)
        boostmarketingplan.impression =request.POST.get('impression')
        boostmarketingplan.cost = request.POST.get('cost')
        boostmarketingplan.description = request.POST.get('description')
        # boostmarketingplan.termsandservices = request.POST.get('termandservice')
        boostmarketingplan.save()
        return redirect('/create_Boostmarketingplan')

class boostmarketingplan(View):
    @method_decorator(login_required(login_url='/adminlogin'))
    def get(self, request):
        boostmarketing = BoostMarketingTable.objects.all()
        # paginator
        paginator=Paginator(boostmarketing,20)
        page_number=request.GET.get('page')
        boostmarketing=paginator.get_page(page_number)
        obj=paginator.page_range
        context = {
            "boostmarketing":boostmarketing, "obj":obj
        }
        return render(request, "boostmarktingplantableView.html", context)

class detailboostmarketingplan(View):
    @method_decorator(login_required(login_url='/adminlogin'))
    def get(self, request, id):
        boostmarketing = BoostMarketingTable.objects.get(id=id)
        context = {
            "boostmarketing":boostmarketing
        }
        return render(request, "detailboostmarketing.html", context)

class Plan_Marketing_Form(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated]
    def create(self, request):
        # print(request.POST)
        serializer=BoostMarkitingTableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(util.success(self,"Created"))
        return Response(util.error(self,"data not found"))

    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            BoostMarketingTableobj=BoostMarketingTable.objects.get(id=id)
            serializer=BoostMarkitingTableSerializer(BoostMarketingTableobj)
            if serializer.data:
                return Response(util.success(self,serializer.data))
            else:
                return Response(util.error(self,"No data found."))
        else:
            return Response(util.error(self,"ID not found."))

class TermsAndServices(APIView):
    def get(self, request, format = None, num = None):
        try:
            if num is not None:
                boostmarketingplanobj = Plan_Type.objects.get(plan_type = num)
                serializer=BoostMarkitingPlanTermsandServicesSerializer(boostmarketingplanobj)
                if serializer.data:
                    return Response(util.success(self,serializer.data))
                else:
                    return Response(util.error(self,'No Data Found'))
            else:
                return Response(util.error(self,'Invalid plan type'))
        except Exception as e:
            return Response(util.error(self,str(e)))