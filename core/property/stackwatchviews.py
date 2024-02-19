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
from accounts.views import get_user_usertype_userprofile
from .serializer import *
from datetime import datetime,timedelta,date
from django.utils import timezone
from master import util
from django.db.models import Count, F
from django.db.models.functions import ExtractMonth, ExtractYear, ExtractWeek, ExtractDay, ExtractWeekDay

# class Daywise(APIView):
#     # permission_classes = [IsAuthenticated]
#     def post(self, request, format=None):
#         data=request.data
#         if 'user_id' in data and 'date' in data:
#             user,usertype,userprofile=get_user_usertype_userprofile(request,data['user_id'])
#             if userprofile:
#                 city_obj=CityMaster.objects.filter(is_active=True)
#                 userprobileobj=Property_Detail.objects.filter(user_profile=userprofile,property_city__in=city_obj)
#                 # # print(data['date']) #2022-12-24
#                 dateobj=datetime.strptime(data['date'], '%Y-%m-%d')
#                 weekday = dateobj.isoweekday()
#                 startdate = dateobj - timedelta(days=weekday)
#                 daywiseproperty=userprobileobj.filter(created_date__gte=startdate, created_date__lte=dateobj).annotate(count=Count('created_date')).values('created_date','property_city' ,'count')
#                 # print(daywiseproperty)
#                 return Response(util.success(self, daywiseproperty))
#             else:
#                 return Response(util.error(self, 'No Data Found'))
#         else:
#             return Response(util.error(self, 'user_id, date is needed'))

class Daywise(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            data=request.data
            if 'user_id' in data and 'date' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['user_id'])
                if userprofile:
                    area_obj=AreaMaster.objects.filter(is_active=True)
                    dateobj=datetime.strptime(data['date'], '%Y-%m-%d')
                    startdate = dateobj - timedelta(days=dateobj.isoweekday())
                    daywiseproperty=Property_Detail.objects.filter(user_profile=userprofile,property_area__in=area_obj,created_date__gte=startdate, created_date__lte=dateobj)
                    daywiseproperty = daywiseproperty.annotate(day = ExtractWeekDay('created_date'))
                    daily_counts = daywiseproperty.values('day','property_area').annotate(count=Count('id'))
                    daily = {}
                    for i in daily_counts:
                        areaobj = AreaMaster.objects.get(id = i['property_area'])
                        daily['property_area']=areaobj.area_name
                        day = i['day']-1
                        days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
                        daily['day']=days[day]
                        daily['count']=i['count']
                    return Response(util.success(self, [daily]))
                else:
                    return Response(util.error(self, 'No Data Found'))
            else:
                return Response(util.error(self, 'user_id, date is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

def week_number_of_month(date_value):
    return (date_value.isocalendar()[1] - date_value.replace(day=1).isocalendar()[1] + 1)

# class Weekwise(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self, request, format=None):
#         try:
#             data=request.data
#             if 'user_id' in data and 'date' in data:
#                 user,usertype,userprofile=get_user_usertype_userprofile(request,data['user_id'])
#                 if userprofile:
#                     weekwiseproperty = Property_Detail.objects.filter(user_profile=userprofile ,created_date__lte = data['date'])
#                     weekwiseproperty = weekwiseproperty.annotate(week=ExtractWeek('created_date'),month=ExtractMonth('created_date'), year=ExtractYear('created_date'))
#                     weekly_counts = weekwiseproperty.values('week','month','year').annotate(count=Count('id'))
#                     return Response(util.success(self, weekly_counts))
#                     # # # print(data['date']) #2022-12-24
#                     # dateobj=datetime.strptime(data['date'], '%Y-%m-%d')
#                     # # week_number=week_number_of_month(dateobj)
#                     # week_number = dateobj.isocalendar()[1]
#                     # # print(week_number)
#                     # # MyModel.objects.filter(date__week=week_number).annotate(week=TruncWeek('date')).values('week').annotate(count=Count('id')).order_by('week')
#                     # # (created_date__week=week_number).annotate(week=F('created_date__week')).values('week').annotate(count=Count('id')).order_by('week')
#                     # # weekwiseproperty=userprobileobj.filter(created_date__week=week_number).annotate(week=TruncWeek('created_date')).values('week').annotate(count=Count('id')).order_by('week')
#                     # weekwiseproperty=userprobileobj.filter(created_date__week=week_number).annotate(week=F('created_date__week')).values('week').annotate(count=Count('created_date')).order_by('week')
#                     # # print(weekwiseproperty)
#                     # return Response(util.success(self, monthly_counts))
#                 else:
#                     return Response(util.error(self, 'No Data Found'))
#             else:
#                 return Response(util.error(self, 'user_id, date is needed'))
#         except Exception as e:
#             return Response(util.error(self,str(e)))

class Weekwise(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            data=request.data
            if 'user_id' in data and 'date' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['user_id'])
                if userprofile:
                    dateobj = datetime.strptime(data['date'], '%Y-%m-%d')
                    week_number = dateobj.isocalendar()[1]
                    first_day_of_week = dateobj - timedelta(days=dateobj.weekday())
                    last_day_of_week = first_day_of_week + timedelta(days=6)
                    weekwiseproperty = Property_Detail.objects.filter(
                        user_profile=userprofile,
                        created_date__range=[first_day_of_week, last_day_of_week]
                    )
                    # weekwiseproperty = Property_Detail.objects.filter(user_profile=userprofile ,created_date__lte = data['date'])
                    weekwiseproperty = weekwiseproperty.annotate(week=ExtractWeek('created_date'),month=ExtractMonth('created_date'), year=ExtractYear('created_date'))
                    weekly_counts = weekwiseproperty.values('week','month','year').annotate(count=Count('id'))
                    for entry in weekly_counts:
                        year = entry['year']
                        week_number = entry['week']
                        # start_date = first_day_of_week.strftime('%Y-%m-%d'),
                        # end_date = last_day_of_week.strftime('%Y-%m-%d'),
                        entry['start_date'] = first_day_of_week.strftime('%Y-%m-%d')
                        entry['end_date'] = last_day_of_week.strftime('%Y-%m-%d')
                    return Response(util.success(self, weekly_counts))
                else:
                    return Response(util.error(self, 'No Data Found'))
            else:
                return Response(util.error(self, 'user_id, date is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))

class Monthwise(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            data=request.data
            if 'user_id' in data and 'date' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['user_id'])
                if userprofile:
                    monthwiseproperty = Property_Detail.objects.filter(user_profile=userprofile ,created_date__lte = data['date'])
                    monthwiseproperty = monthwiseproperty.annotate(month=ExtractMonth('created_date'), year=ExtractYear('created_date'))
                    monthly_counts = monthwiseproperty.values('month','year').annotate(count=Count('id'))
                    # print(monthly_counts)
                    monthly = {}
                    for i in monthly_counts:
                        month = i['month']-1
                        months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
                        monthly['month']=months[month]
                        monthly['year'] = i['year']
                        monthly['count']=i['count']
                    return Response(util.success(self, [monthly]))
                else:
                    return Response(util.error(self, "User Not Found"))
            else:
                return Response(util.error(self, "date is required"))
        except Exception as e:
            return Response(util.error(self,str(e)))

class Coustomize_date(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            data=request.data
            if 'user_id' in data and 'Start_date' in data and 'End_date' in data:
                user,usertype,userprofile=get_user_usertype_userprofile(request,data['user_id'])
                if userprofile:
                    dateobj1=datetime.strptime(data['Start_date'], '%Y-%m-%d')
                    dateobj2=datetime.strptime(data['End_date'], '%Y-%m-%d')
                    daywiseproperty=Property_Detail.objects.filter(user_profile=userprofile,created_date__gte=dateobj1, created_date__lte=dateobj2)
                    # # print(data['date']) #2022-12-24
                    daywiseproperty = daywiseproperty.annotate(day = ExtractDay('created_date'))
                    daily_counts = daywiseproperty.values('day','property_city').annotate(count=Count('id'))
                    # print(daywiseproperty)
                    return Response(util.success(self, daily_counts))
                else:
                    return Response(util.error(self, 'No Data Found'))
            else:
                return Response(util.error(self, 'user_id, Start_date, End_date is needed'))
        except Exception as e:
            return Response(util.error(self,str(e)))
