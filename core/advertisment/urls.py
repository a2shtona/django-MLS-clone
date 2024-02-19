from django.urls import path
from .import views


urlpatterns = [
    path('advertismentuserview/',views.AdvertismentUserView.as_view(),name='advertismentuserview'),
    path('advertismentlogin/',views.AdvertismentLogin.as_view(),name='advertismentlogin'),

    path('advertismentsave/',views.AdvertismentSave.as_view(),name='advertismentsave'),
    path('advertismentsave/<int:id>',views.AdvertismentSave.as_view(),name='advertismentsave'),

]