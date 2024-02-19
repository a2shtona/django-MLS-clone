from pyexpat import model
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import *
from accounts.views import get_user_usertype_userprofile
from .serializer import *
from django.http import HttpResponse, JsonResponse
import json
from . import util

class CountryView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request, format=None):
        try:
            data=request.data
            if 'user_id' in data and 'country_code' in data and 'country_name' in data and "position" in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['user_id'])
                if user:
                    if usertype.user_type == 0:
                        if CountryMaster.objects.filter(country_code=data['country_code']) or CountryMaster.objects.filter(country_name=data['country_name']):
                            # return Response({'msg':"Country Code or Country Name is Already Exists"})
                            return Response(util.error(self,'Country Code or Country Name is Already Exists'))
                        else:
                            CountryMaster.objects.create(country_code=data['country_code'],country_name=data['country_name'],is_active=True,position=data['position'])
                            # return Response({'msg':"Country Created Successfully"})
                            return Response(util.success(self,'Country Created Successfully'))
                    else:
                        # return Response({'msg':'Not a Valid User To Do Entry'})
                        return Response(util.error(self,'Not a Valid User To Do Entry'))
                else:
                    # return Response({'msg':'User Id is Not Valid'})
                    return Response(util.error(self,'User Id is Not Valid'))
                # return Response({'msg':'Country Created'})
                return Response(util.error(self,'Country Created'))
            else:
                # return Response({'msg':'user_id, country_code, country_name, position is needed'})
                return Response(util.error(self,'user_id, country_code, country_name, position is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

    def get(self,request, format=None, id=None):
        try:
            if id is not None:
                if CountryMaster.objects.filter(id=id):
                    country=CountryMaster.objects.get(id=id)
                    serializer=CountrySerializer(country)
                    # return JsonResponse(serializer.data,safe=False)
                    if serializer.data:
                        return Response(util.success(self,serializer.data))
                    else:
                        return Response(util.error(self, 'No Data Found'))
                else:
                    # return Response({'msg':'Country Id Not Match'})
                    return Response(util.error(self,'Country Id Not Match'))
            else:
                allcountry=CountryMaster.objects.all()
                serializer=CountrySerializer(allcountry, many=True)
                # return JsonResponse(serializer.data, safe=False)
                return Response(util.success(self, serializer.data))
        except Exception as e:
            return Response(util.error(self,str(e)))

class StateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        try:
            data=request.data
            if 'user_id' in data and 'country_id' in data and 'state_name' in data and 'position' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['user_id'])
                if user:
                    if usertype.user_type == 0:
                        if CountryMaster.objects.filter(id=data['country_id']):
                            countrymasterobj=CountryMaster.objects.get(id=data['country_id'])
                            StateMaster.objects.create(country_master=countrymasterobj,state_name=data['state_name'],position=data['position'])
                        else:
                            # return Response({'msg':'Country Not Found'})
                            return Response(util.error(self,'Country Not Found'))
                    else:
                        # return Response({'msg':'Not a Valid User To Do Entry'})
                        return Response(util.error(self,'Not a Valid User To Do Entry'))
                else:
                    # return Response({'msg':'User Id is Not Valid'})
                    return Response(util.error(self,'User Id is Not Valid'))
                # return Response({'msg':'State Created'})
                return Response(util.success(self,'State Created'))
            else:
                # return Response({'msg':'user_id, country_id, state_name is needed'})
                return Response(util.error(self,'user_id, country_id, state_name is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))
    
    def get(self,request, format=None, id=None):
        try:
            if id is not None:
                if StateMaster.objects.filter(id=id):
                    state=StateMaster.objects.get(id=id)
                    serializer=StateSerializer(state)
                    # return JsonResponse(serializer.data,safe=False)
                    if serializer.data:
                        return Response(util.success(self,serializer.data))
                    else:
                        return Response(util.error(self, 'No Data Found'))
                else:
                    # return Response({'msg':'Country Id Not Match'})
                    return Response(util.error(self,'Country Id Not Match'))
            else:
                allstates=StateMaster.objects.all()
                serializer=StateSerializer(allstates, many=True)
                # return JsonResponse(serializer.data, safe=False)
                return Response(util.success(self, serializer.data))
        except Exception as e:
            return Response(util.error(self,str(e)))
  
class CityView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        try:
            data=json.loads(request.body)
            if 'user_id' in data and 'state_id' in data and 'city_name' in data  and 'position' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['user_id'])

                if user:
                    if usertype.user_type == 0:
                        if StateMaster.objects.filter(id=data['state_id']):
                            statemasterobj=StateMaster.objects.get(id=data['state_id'])
                            CityMaster.objects.create(state_master=statemasterobj,city_name=data['city_name'], position=data['position'])
                        else:
                            # return Response({'msg':'State Not Found'})
                            return Response(util.error(self,'State Not Found'))
                    else:
                        # return Response({'msg':'Not a Valid User To Do Entry'})
                        return Response(util.error(self,'Not a Valid User To Do Entry'))
                else:
                    # return Response({'msg':'User Id is Not Valid'})
                    return Response(util.error(self,'User Id is Not Valid'))
                # return Response({'msg':'City Created'})
                return Response(util.success(self,'City Created'))
            else:
                # return Response({'msg':'user_id, state_id, state_name is needed'})
                return Response(util.error(self,'user_id, state_id, state_name is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))
    
    def get(self,request, format=None, id=None):
        try:
            if id is not None:
                if CityMaster.objects.filter(id=id):
                    city=CityMaster.objects.get(id=id)
                    serializer=CitySerializer(city)
                    if serializer.data:
                        return Response(util.success(self,serializer.data))
                    else:
                        return Response(util.error(self, 'No Data Found'))
                else:
                    return Response(util.error(self,'Country Id Not Match'))
            else:
                allcity=CityMaster.objects.all()
                serializer=CitySerializer(allcity, many=True)
                return Response(util.success(self,serializer.data))
        except Exception as e:
            return Response(util.error(self,str(e)))

class ZipCode(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        try:
            data=json.loads(request.body)
            if 'user_id' in data and 'area_id' in data and 'zip_code' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['user_id'])
                if user:
                    if usertype.user_type == 0:
                        if AreaMaster.objects.filter(id=data['area_id']):
                            areamasterobj=AreaMaster.objects.get(id=data['area_id'])
                            ZipCodeMaster.objects.create(area_master=areamasterobj,Zipcode=data['zip_code'],)
                        else:
                            return Response({'msg':'City Not Found'})
                    else:
                        return Response({'msg':'Not a Valid User To Do Entry'})
                else:
                    return Response({'msg':'User Id is Not Valid'})
                return Response({'msg':'Zipcode Created'})
            else:
                return Response({'msg':'user_id, city_id, zip_code is needed'})
        except Exception as e:
            return Response(util.error(self,str(e)))

    def get(self,request, format=None, id=None):
        try:
            if id is not None:
                if ZipCodeMaster.objects.filter(id=id):
                    zip=ZipCodeMaster.objects.get(id=id)
                    serializer=ZipcodeSerializer(zip)
                    return Response(util.success(self,serializer.data))
                else:
                    return Response(util.error(self,'Area Id Not Match'))
            else:
                allzip=ZipCodeMaster.objects.values("Zipcode").distinct()
                # allzip=ZipCodeMaster.objects.all()
                serializer=ZipcodeSerializer(allzip, many=True)
                if serializer.data:
                    return Response(util.success(self,serializer.data))
                else:
                    return Response(util.error(self,'Data Not Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class AreaZipcode(APIView):
    def get(self, request, format = None, id = None):
        try:
            if id is not None:
                if AreaMaster.objects.filter(id__in = id): # Area Id is Filter
                    areaobj = AreaMaster.objects.get(id = id) # Get Area Id
                    zipcodeobj = ZipCodeMaster.objects.filter(area_master__in = areaobj).values('Zipcode').distinct()
                    serializer = ZipcodeSerializer(zipcodeobj,many=True)
                    if serializer.data:
                        return Response(util.success(self,serializer.data))
                    else:
                        return Response(util.error(self, "Data Not Found"))
                else:
                    return Response(util.error(self, "Data Not Found"))
            else:
                return Response(util.error(self, "id is required"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class Area(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        try:
            data=json.loads(request.body)
            if 'user_id' in data and 'zip_code_id' in data and 'city_id' in data and 'area_name' in data: 
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['user_id'])
                if user:
                    if usertype.user_type == 0:
                        if CityMaster.objects.filter(id=data['city_id']) and ZipCodeMaster.objects.filter(id=data['zip_code_id']):
                            citymasterobj=CityMaster.objects.get(id=data['city_id'])
                            zipcodeobj=ZipCodeMaster.objects.get(id=data['zip_code_id'])
                            AreaMaster.objects.create(zip_code_master=zipcodeobj,city_master=citymasterobj,area_name=data['area_name'],)
                        else:
                            # return Response({'msg':'City or Zipcode Not Found'})
                            return Response(util.error(self,'City or Zipcode Not Found'))
                    else:
                        # return Response({'msg':'Not a Valid User To Do Entry'})
                        return Response(util.error(self,'Not a Valid User To Do Entry'))
                else:
                    # return Response({'msg':'User Id is Not Valid'})
                    return Response(util.error(self,'User Id is Not Valid'))
                # return Response({'msg':'Area Created'})
                return Response(util.success(self,'Area Created'))
            else:
                # return Response({'msg':'user_id, city_id, zip_code_id, area_name is needed'})
                return Response(util.error(self,'user_id, city_id, zip_code_id, area_name is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

    def get(self,request, format=None, id=None):
        try:
            if id is not None:
                if AreaMaster.objects.filter(id=id):
                    zip=AreaMaster.objects.get(id=id)
                    serializer=AreaSerializer(zip)
                    # return JsonResponse(serializer.data,safe=False)
                    return Response(util.success(self,serializer.data))
                else:
                    # return Response({'msg':'Country Id Not Match'})
                    return Response(util.error(self,'Area Id Not Match'))
            else:
                allzip=AreaMaster.objects.all()
                serializer=AreaSerializer(allzip, many=True)
                # return JsonResponse(serializer.data, safe=False)
                if serializer.data:
                    return Response(util.success(self,serializer.data))
                else:
                    return Response(util.error(self,'Data Not Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class GetState(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request, format=None):
        try:
            data=json.loads(request.body)
            if "country_id" in data:
                if CountryMaster.objects.filter(id=data['country_id']):
                    countrymasterobj=CountryMaster.objects.get(id=data['country_id'])
                    statemaster=StateMaster.objects.filter(country_master=countrymasterobj)
                    serializer=StateSerializer(statemaster, many=True)
                    if serializer.data:
                        return Response(util.success(self,serializer.data))
                    else:
                        return Response(util.error(self,'Data Not Found'))
                else:
                    return Response(util.error(self,'Country Not Found'))
            else:
                return Response(util.error(self,'country_id is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class GetCity(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request, format=None):
        try:
            data=json.loads(request.body)
            if "state_id" in data:
                if StateMaster.objects.filter(id=data['state_id']):
                    statemasterobj=StateMaster.objects.get(id=data['state_id'])
                    citymaster=CityMaster.objects.filter(state_master=statemasterobj)
                    serializer=CitySerializer(citymaster, many=True)
                    if serializer.data:
                        return Response(util.success(self,serializer.data))
                    else:
                        return Response(util.error(self,'Data Not Found'))
                else:
                    return Response(util.error(self,'Country Not Found'))
            else:
                return Response(util.error(self,'state_id is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class GetArea(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request, format=None):
        try:
            data=json.loads(request.body)
            if "city_id" in data:
                if CityMaster.objects.filter(id=data['city_id']):
                    citymasterobj=CityMaster.objects.get(id=data['city_id'])
                    citymaster=AreaMaster.objects.filter(city_master=citymasterobj)
                    serializer=AreaSerializer(citymaster, many=True)
                    if serializer.data:
                        return Response(util.success(self,serializer.data))
                    else:
                        return Response(util.error(self,'Data Not Found'))
                else:
                    return Response({'msg':'Country Not Found'})
            else:
                # return Response({'msg':'city_id is required'})
                return Response(util.error(self,'city_id is required'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class PetViewAPI(APIView):
    def get(self, request, format=None):
        try:
            petobj=PetMaster.objects.all()
            serializer=PetSerializer(petobj, many=True)
            if serializer.data:
                return Response(util.success(self,serializer.data))
            else:
                return Response(util.error(self,'Data Not Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

#loadlanguage
class loadLanguageView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            loadlanguageobj=LanguageMaster.objects.all()
            serializer=loadLanguageSerializer(loadlanguageobj, many=True)
            if serializer.data:
                return Response(util.success(self,serializer.data))
            else:
                return Response(util.error(self,'Data Not Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

#loadstate&city
class LoadcityareaView(APIView):
    def get(self, request, format=None):
        try:
            citymaster=CityMaster.objects.all().order_by('position')
            serialize=citymasterSerializer(instance=citymaster, many=True)
            if serialize.data:
                return Response(util.success(self,serialize.data))
            else:
                return Response(util.error(self,'Data Not Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class SubscriptionplanView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            user_type = request.GET.get('user_type')
            serviceplanobj=SubscriptionPlanServices.objects.filter(UserType = user_type)
            # serviceplanobj=SubscriptionPlanServices.objects.all()
            serializer=SubscriptionplanSerializer(serviceplanobj, many=True)
            # # print(serializer.data)
            if serializer.data:
                return Response(util.success(self,serializer.data))
            else:
                return Response(util.error(self,'Data Not Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class ServiceView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            user_type = request.GET.get('user_type')
            serviceplanobj=SubscriptionServices.objects.filter(usertype=user_type)
            # serviceplanobj=SubscriptionServices.objects.filter(usertype=2)
            serializer=ServiceSerializer(serviceplanobj, many=True)
            if serializer.data:
                return Response(util.success(self,serializer.data))
            else:
                return Response(util.error(self,'Data Not Found'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class SubscriptionServicesview(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            data=request.data
            # print(data)
            if 'service_id' in data:
                subscriptionserviceobj=SubscriptionServices.objects.all()
                service_dict={}
                for  i in subscriptionserviceobj:
                    if i.id in data['service_id']:
                        service_dict[i.service_name]=True
                    else:
                        service_dict[i.service_name]=False
                return Response(util.success(self, service_dict)) 
            else:
                return Response(util.error(self,"service_id is needed" ))
        except Exception as e:
            return Response(util.error(self,str(e)))

# class StatewiseCity(APIView):
#     def get(self, request, format=None, id=None):
#         try:
#             if id is not None:
#                 stateobj = StateMaster.objects.get(id = id)
#                 cityobj = CityMaster.objects.filter(state_master = stateobj)
#                 serializer = CitySerializer(cityobj, many=True).data
#                 return Response(util.success(self, serializer))
#             else:
#                 return Response(util.error(self, "id is required"))
#         except Exception as e:
#             return Response(util.error(self,str(e)))

# class CityWiseArea(APIView):
#     def get(self, request, format=None, id=None):
#         try:
#             if id is not None:
#                 cityobj = CityMaster.objects.get(id = id)
#                 areaobj = AreaMaster.objects.filter(city_master = cityobj)
#                 serializer = AreaSerializer(areaobj, many=True).data
#                 return Response(util.success(self, serializer))
#             else:
#                 return Response(util.error(self, "id is required"))
#         except Exception as e:
#             return Response(util.error(self,str(e)))