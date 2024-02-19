
from django.urls import path
from .import views
from .adminview import *
from . import masterviews as aview

urlpatterns = [

# =========================================== NewTemplate ==========================================
    path('AdminDashboard/',AdminDashboard.as_view(),name='AdminDashboard'),
    path('ProfilePage/',ProfilePage.as_view(),name='ProfilePage'),
    path('GeoDataBasePage/',GeoDataBasePage.as_view(),name='GeoDataBasePage'),
    path('Toolspage/',Toolspage.as_view(),name='Toolspage'),
    path('VerficationDashboard/',VerficationDashboard.as_view(),name='VerficationDashboard'),
    # path('AllProfileDashboard/',AllProfileDashboard.as_view(),name='AllProfileDashboard'),
    path('BoostMarketingAdminDashBoard/',BoostMarketingAdminDashBoard.as_view(),name='BoostMarketingAdminDashBoard'),
    path('BoosMarketingAddAdmin/',BoosMarketingAddAdmin.as_view(),name='BoosMarketingAddAdmin'),
    path('ProfileInDetails/<int:id>',ProfileInDetails.as_view(),name='ProfileInDetails'),
    path('AddPropertyLIstingTypeView/',AddPropertyLIstingTypeView.as_view(),name='AddPropertyLIstingTypeView'),
    path('SublistingView/',SublistingView.as_view(),name='SublistingView'),
    path('AddTermsView/',AddTermsView.as_view(),name='AddTermsView'),
    path('AddOffersView/',AddOffersView.as_view(),name='AddOffersView'),
    # path('Basictemplate/',Basictemplate.as_view(),name='Basictemplate'),

    # Data Comes from API User
    path('Api_AllUser/',Api_AllUser.as_view(),name='Api_AllUser'),
    path('Api_GuestUser/',Api_GuestUser.as_view(),name='Api_GuestUser'),
    path('Api_AgentUser/',Api_AgentUser.as_view(),name='Api_AgentUser'),
    path('Api_InvestorUser/',Api_InvestorUser.as_view(),name='Api_InvestorUser'),
    path('Api_FsbhoUser/',Api_FsbhoUser.as_view(),name='Api_FsbhoUser'),
    path('Api_ManagementUser/',Api_ManagementUser.as_view(),name='Api_ManagementUser'),
    path('Api_SubAgentUser/',Api_SubAgentUser.as_view(),name='Api_SubAgentUser'),
    path('Api_BoostMarketingUser/',Api_BoostMarketingUser.as_view(),name='Api_BoostMarketingUser'),
    path('Api_AdvertisementUser/',Api_AdvertisementUser.as_view(),name='Api_AdvertisementUser'),
    path('Api_InactiveUser/',Api_InactiveUser.as_view(),name='Api_InactiveUser'),
    path('API_Neighborhood/',API_Neighborhood.as_view(),name='API_Neighborhood'),
    path('API_AgentLic/',API_AgentLic.as_view(),name='API_AgentLic'),
    path('API_AllSupportList/',API_AllSupportList.as_view(),name='API_AllSupportList'),
    path('API_AgentSupportList/',API_AgentSupportList.as_view(),name='API_AgentSupportList'),
    path('API_GuestSupportList/',API_GuestSupportList.as_view(),name='API_GuestSupportList'),

    # Data Comes from API Location
    path('API_Country/',API_Country.as_view(),name='API_Country'),
    path('API_State/',API_State.as_view(),name='API_State'),
    path('API_City/',API_City.as_view(),name='API_City'),
    path('API_Area/',API_Area.as_view(),name='API_Area'),
    path('API_ZipCode/',API_ZipCode.as_view(),name='API_ZipCode'),

    # Data Comes from API Language
    path('API_LanguageList/',API_LanguageList.as_view(),name='API_LanguageList'),

    # Data Comes from API Terms
    path('API_TermsList/',API_TermsList.as_view(),name='API_TermsList'),
    path('API_OfferList/',API_OfferList.as_view(),name='API_OfferList'),

    # Data Comes From Api HomeCard
    path('API_HomeCardList/',API_HomeCardList.as_view(),name='API_HomeCardList'),


    path('AdminBasicPage/',AdminBasicPage.as_view(),name='AdminBasicPage'),


    path('PropertyListingAdminShow/',PropertyListingAdminShow.as_view(),name='PropertyListingAdminShow'),
    path('PropertyListingTypeAdminShow/',PropertyListingTypeAdminShow.as_view(),name='PropertyListingTypeAdminShow'),
    path('PropertyMainCategoryAdminShow/',PropertyMainCategoryAdminShow.as_view(),name='PropertyMainCategoryAdminShow'),
    path('PropertySubCategoryAdminShow/',PropertySubCategoryAdminShow.as_view(),name='PropertySubCategoryAdminShow'),


# =========================================== Old Template ==========================================
    path('AgentSupportView/',AgentSupportView.as_view(),name='AgentSupportView'),
    path('AgentSupportView/<int:id>',AgentSupportView.as_view(),name='AgentSupportView'),
    path('GuestSupportView/',GuestSupportView.as_view(),name='GuestSupportView'),
    path('GuestSupportView/<int:id>',GuestSupportView.as_view(),name='GuestSupportView'),
    path('AddLocation/',AddLocation.as_view(),name='AddLocation'), 
    path('Uploadlanguage/',Uploadlanguage.as_view(),name='Uploadlanguage'), 

    path('country/',views.CountryView.as_view(),name='country'), 
    path('country/<int:id>',views.CountryView.as_view(),name='country'), 

    path('state/',views.StateView.as_view(),name='state'),
    path('state/<int:id>',views.StateView.as_view(),name='state'), 

    path('city/',views.CityView.as_view(),name='city'), 
    path('city/<int:id>',views.CityView.as_view(),name='city'), 

    path('zipcode/',views.ZipCode.as_view(),name='zipcode'),
    path('zipcode/<int:id>',views.ZipCode.as_view(),name='zipcode'), 
    
    path('area/',views.Area.as_view(),name='area'),
    path('area/<int:id>',views.Area.as_view(),name='area'),

    path('AreaZipcode/<int:id>',views.AreaZipcode.as_view(),name='AreaZipcode'),


    path('getstate/',views.GetState.as_view(),name='getstate'),
    path('getcity/',views.GetCity.as_view(),name='getcity'),    
    path('getarea/',views.GetArea.as_view(),name='getarea'),
    path('PetViewAPI/',views.PetViewAPI.as_view(),name='PetViewAPI'),
    path('loadLanguageView/',views.loadLanguageView.as_view(),name='loadLanguageView'),
    path('subscrptionplan/',views.SubscriptionplanView.as_view(),name='subscrptionplan'),
    path('service/',views.ServiceView.as_view(),name='service'),
    # path('StatewiseCity/<int:id>',views.StatewiseCity.as_view(),name='StatewiseCity'),
    # path('CityWiseArea/<int:id>',views.CityWiseArea.as_view(),name='CityWiseArea'),


    #admin url
    path('',AdminLogin.as_view(),name='adminlogin'),
    # path('adminlogin',AdminLogin.as_view(),name='adminlogin'),
    path('prodev-adminregister',superuserregistrations,name='adminregister'),

    path('verify-email',SendVerifucationMail.as_view(),name='verifyemail'),
    path('dashboard',Dashboard.as_view(),name='dashboard'),
    path('userlist',UserList.as_view(),name='userlist'),
    path('logout',LogoutView.as_view(),name='logout'),
    path('userprofile/<int:id>',UserProfileView.as_view(),name='userprofile'),
    path('blockuser/<int:pk>',BlockUser.as_view(),name='blockuser'),
    path('unblockuser/<int:pk>',UnBlockUser.as_view(),name='unblockuser'),
    path('suspenduser/<int:pk>',SuspendUser.as_view(),name='suspenduser'),
    
    # property Detail
    path('list_view',Property_list_view.as_view(),name='list_view'),
    path('detail_view/<int:id>',DetailView.as_view(),name='detail_view'),


    path('typeoflisting',AddTypeOfListing.as_view(),name='typeoflisting'),
    path('typeoflisting/<int:id>',AddTypeOfListing.as_view(),name='typeoflisting'),
    path('updatetypeoflisting/<int:id>',UpdateTypeOfListing.as_view(),name='updatetypeoflisting'),

    #Property Main Category Urls
    path('propertymaincategory',PropertyMainCategory.as_view(),name='propertymaincategory'),
    path('propertymaincategory/<int:id>',PropertyMainCategory.as_view(),name='propertymaincategory'),
    path('editpropertymaincategory/<int:pk>',EditPropertyMainCategory.as_view(),name='editpropertymaincategory'),

    #Property Sub Category URLS
    path('propertysubcategorylist',PropertySubCategory.as_view(),name='propertysubcategorylist'),
    path('propertysubcategorylist/<int:id>',PropertySubCategory.as_view(),name='propertysubcategorylist'),
    path('editpropertysubcategory/<int:id>',EditPropertySubCategory.as_view(),name='editpropertysubcategory'),
    
    #Property Type Urls
    path('propertytype',PropertyType.as_view(),name='propertytype'),
    path('propertytype/<int:id>',PropertyType.as_view(),name='propertytype'),
    path('editpropertytype/<int:id>',EditPropertyType.as_view(),name='editpropertytype'),

    #Property Aminity Urls
    path('property-aminities',AdminPropertyAminites.as_view(),name='property-aminities'),
    path('propertyaminitydelete/<int:id>',PropertyAminityDelete.as_view(),name='propertyaminitydelete'),
    path('propertyaminityedit/<int:id>',PropertyAminityEdit.as_view(),name='propertyaminityedit'),

    #State Master Urls
    path('statemaster',StateMasterView.as_view(),name='statemaster'),
    path('deletestatemaster/<int:id>',DeleteStateMasterView.as_view(),name='deletestatemaster'),
    path('editstatemaster/<int:id>',EditStateMasterView.as_view(),name='editstatemaster'),

    #City Master Url
    path('citymaster',CityMasterView.as_view(),name='citymaster'),
    path('deletecitymaster/<int:id>',DeleteCityMasterView.as_view(),name='deletecitymaster'),
    path('editcitymaster/<int:id>',EditCityMasterView.as_view(),name='editcitymaster'),

    #Language Master Url
    path('languagemaster',LanguageMasterView.as_view(),name='languagemaster'),
    path('deletelanguage/<int:id>',Deletelanguage.as_view(),name='deletelanguage'),
    # path('deletelanguagemaster/<int:id>',DeleteLanguageMasterView.as_view(),name='deletelanguagemaster'),
    path('editlanguagemaster/<int:id>',EditLanguageMasterView.as_view(),name='editlanguagemaster'),

    #Agent License Pending Reuqest
    path('agentpendingrequest',Agent_Lic_Pending_Reuqest.as_view(),name='agentpendingrequest'),
    path('agentpendingrequest/<int:id>',Agent_Lic_Pending_Reuqest.as_view(),name='agentpendingrequest'),

    #Agent License Approved
    path('agentapprovedrequest',Agent_Lic_Approved_Reuqest.as_view(),name='agentapprovedrequest'),

    path('neighborhoodpendingrequest/',Agent_Neighborhood_Specialist_Panding_request.as_view(), name="neighborhoodpendingrequest"),
    path('neighborhoodpendingrequest/<int:id>',Agent_Neighborhood_Specialist_Panding_request.as_view(), name="neighborhoodpendingrequest"),
    path('Neighborhood_Approved',Neighborhood_Approved.as_view(),name='Neighborhood_Approved'),

    # luxary amount
    # sales
    path('luxarysalesamt',luxarysalesamt.as_view(),name='luxarysalesamt'),
    path('luxarysalesamt/<int:id>',luxarysalesamt.as_view(),name='luxarysalesamt'),
    # rent
    path('luxaryrentamt',luxaryrentamt.as_view(),name='luxaryrentamt'),
    path('luxaryrentamt/<int:id>',luxaryrentamt.as_view(),name='luxaryrentamt'),

    path('guestlist',GuestList.as_view(),name='guestlist'),
    path('agenttlist',AgentList.as_view(),name='agenttlist'),
    path('investorDevloperlist',InvestorDevloperlist.as_view(),name='investorDevloperlist'),
    path('fsbholist',FSBHOlist.as_view(),name='fsbholist'),
    path('managementlist',ManagementList.as_view(),name='managementlist'),


    path('property-settings',PropertySettings.as_view(),name='propertySettings'),
    path('location-master',LocationMaster.as_view(),name='locationmaster'),
    path('subscription-services',SubscriptionServicesView.as_view(),name='subscription-services'),
    path('editsubscriptionservices/<int:id>',EditSubscriptionServices.as_view(),name='editsubscriptionservices'),
    path('deletesubscriptionservices/<int:id>',DeleteSubscriptionService.as_view(),name='deletesubscriptionservices'),



    path('subscription-plan',SubscriptionPlanView.as_view(),name='subscription-plan'),
    path('subscription-plan/<int:id>',SubscriptionPlanView.as_view(),name='subscription-plan'),
    path('subscription-plan-update/<int:id>',SubscriptionPlanUpdate.as_view(),name='subscription-plan-update'),
    
    path('agentlicview',AgentLicView.as_view(),name='agentlicview'),
    path('agentlicdelete/<int:id>',AgentLicDelete.as_view(),name='agentlicdelete'),
    path('searchforhome/', aview.SearchForHome.as_view(), name="searchforhome"),
    path('AreaSearch/', aview.AreaSearch.as_view(), name="AreaSearch"),
    path('ZipSerach/', aview.ZipSerach.as_view(), name="ZipSerach"),
    path('loadcityareaView/',views.LoadcityareaView.as_view(), name='loadcityarea'),

    path('subscriptionservices/',views.SubscriptionServicesview.as_view(), name='subscriptionservices'),


    path('AddBoostmarketingAdmin/',AddBoostmarketingAdmin.as_view(), name='AddBoostmarketingAdmin'),
    path('BoostMarketingAdminAll',BoostMarketingAdminAll.as_view(), name='BoostMarketingAdminAll'),
    path('DeleteBoostMarketingAdmin/<int:id>',DeleteBoostMarketingAdmin.as_view(), name='DeleteBoostMarketingAdmin'),

  

    # New Url
    path('DeleteTerms/<int:id>',DeleteTerms.as_view(), name='DeleteTerms'),
    path('DeleteOffer/<int:id>',DeleteOffer.as_view(), name='DeleteOffer'),
    path('homecarddelete/<int:id>',HomeCardDelete.as_view(),name='homecarddelete'),
    path('homecardtitldelete/<int:id>',HomeCardTitleDelete.as_view(),name='homecardtitldelete'), 

    path('MainCategorylisting',MainCategorylisting.as_view(),name='MainCategorylisting'), 

    path('AdminCountryMasterDelete/<int:id>',AdminCountryMasterDelete.as_view(),name='AdminCountryMasterDelete'), 
    
    path('AddCountryAdmin',AddCountryAdmin.as_view(),name='AddCountryAdmin'),
    path('AddCountryAdmin/<int:id>',AddCountryAdmin.as_view(),name='AddCountryAdmin'),

    path('AddStateAdmin',AddStateAdmin.as_view(),name='AddStateAdmin'),
    path('AddStateAdmin/<int:id>',AddStateAdmin.as_view(),name='AddStateAdmin'),

    path('AddCityAdmin',AddCityAdmin.as_view(),name='AddCityAdmin'),
    path('AddCityAdmin/<int:id>',AddCityAdmin.as_view(),name='AddCityAdmin'),

    path('AddAreaAdmin',AddAreaAdmin.as_view(),name='AddAreaAdmin'),
    path('AddAreaAdmin/<int:id>',AddAreaAdmin.as_view(),name='AddAreaAdmin'),

    path('AddZipAdmin',AddZipAdmin.as_view(),name='AddZipAdmin'),
    path('AddZipAdmin/<int:id>',AddZipAdmin.as_view(),name='AddZipAdmin'),

    path('AdminApprovedAgentNbSpeciality/<int:id>',AdminApprovedAgentNbSpeciality.as_view(),name='AdminApprovedAgentNbSpeciality'),
    path('AdminRejectedAgentNbSpeciality/<int:id>',AdminRejectedAgentNbSpeciality.as_view(),name='AdminRejectedAgentNbSpeciality'),


    path('AdminHomeCardTitle',AdminHomeCardTitle.as_view(),name='AdminHomeCardTitle'),
    path('AdminHomeCardAdd',AdminHomeCardAdd.as_view(),name='AdminHomeCardAdd'),


    path('AdminApprovedAgentLic/<int:id>',AdminApprovedAgentLic.as_view(),name='AdminApprovedAgentLic'),
    path('AdminRejectAgentLic/<int:id>',AdminRejectAgentLic.as_view(),name='AdminRejectAgentLic'),


    path('AdminBlockUser/<int:pk>',AdminBlockUser.as_view(),name='AdminBlockUser'),
    path('AdminUnBlockUser/<int:pk>',AdminUnBlockUser.as_view(),name='AdminUnBlockUser'),
    path('AdminSuspendUser/<int:pk>',AdminSuspendUser.as_view(),name='AdminSuspendUser'),
    path('AdminUnSuspendUser/<int:pk>',AdminUnSuspendUser.as_view(),name='AdminUnSuspendUser'),

    path('UpdateCountryDataAdmin/<int:id>',UpdateCountryDataAdmin.as_view(),name='UpdateCountryDataAdmin'),
    
    path('UpdateLanguageAdmin/<int:id>',UpdateLanguageAdmin.as_view(),name='UpdateLanguageAdmin'),
    path('UpdateHomeCardTitleAdmin/<int:id>',UpdateHomeCardTitleAdmin.as_view(),name='UpdateHomeCardTitleAdmin'),
    path('UpdateHomeCardAdmin/<int:id>',UpdateHomeCardAdmin.as_view(),name='UpdateHomeCardAdmin'),

    path('UploadPropertyDataAdmin',UploadPropertyDataAdmin.as_view(),name='UploadPropertyDataAdmin'),



    path('AddAdminMainListingType',AddAdminMainListingType.as_view(),name='AddAdminMainListingType'),
    path('AddAdminMainListingType/<int:id>',AddAdminMainListingType.as_view(),name='AddAdminMainListingType'),
    path('PropertyMainlistingDelete/<int:id>',PropertyMainlistingDelete.as_view(),name='PropertyMainlistingDelete'),

    path('AddAdminSubListingType',AddAdminSubListingType.as_view(),name='AddAdminSubListingType'),
    path('AddAdminSubListingType/<int:id>',AddAdminSubListingType.as_view(),name='AddAdminSubListingType'),
    path('PropertySublistingDelete/<int:id>',PropertySublistingDelete.as_view(),name='PropertySublistingDelete'),

    path('AddAdminMainCategory',AddAdminMainCategory.as_view(),name='AddAdminMainCategory'),
    path('AddAdminMainCategory/<int:id>',AddAdminMainCategory.as_view(),name='AddAdminMainCategory'),
    path('PropertyMainCategoryDelete/<int:id>',PropertyMainCategoryDelete.as_view(),name='PropertyMainCategoryDelete'),
    
    path('AddAdminSubCategory',AddAdminSubCategory.as_view(),name='AddAdminSubCategory'),
    path('AddAdminSubCategory/<int:id>',AddAdminSubCategory.as_view(),name='AddAdminSubCategory'),
    path('PropertySubCategoryDelete/<int:id>',PropertySubCategoryDelete.as_view(),name='PropertySubCategoryDelete'),


    path('EditSubListingType/',EditSubListingType.as_view(),name='EditSubListingType'),
    path('EditSubListingType/<int:id>',EditSubListingType.as_view(),name='EditSubListingType'),

    path('EditMainCategory/',EditMainCategory.as_view(),name='EditMainCategory'),
    path('EditMainCategory/<int:id>',EditMainCategory.as_view(),name='EditMainCategory'),

    path('SalesDashboard/',SalesDashboard.as_view(),name='SalesDashboard'),

    path('AllSublistingTypeView/', AllSublistingTypeView.as_view(), name='AllSublistingTypeView'),
    path('AllMainCategoryTypeView/', AllMainCategoryTypeView.as_view(), name='AllMainCategoryTypeView'),
    path('AllSubCategoryTypeView/', AllSubCategoryTypeView.as_view(), name='AllSubCategoryTypeView'),

    path('AddPropertylistingAll/', AddPropertylistingAll.as_view(), name='AddPropertylistingAll'),

    path('AdminAddBoostMarketingUser/', AdminAddBoostMarketingUser.as_view(), name='AdminAddBoostMarketingUser'),
    path('AdminSecurityandPassword/', AdminSecurityandPassword.as_view(), name='AdminSecurityandPassword'),

    
    path('AllStateDataName/', AllStateDataName.as_view(), name='AllStateDataName'),
    path('AllCityDataName/', AllCityDataName.as_view(), name='AllCityDataName'),
    path('AllTownDataName/', AllTownDataName.as_view(), name='AllTownDataName'),
    path('AllZipCodeDataName/', AllZipCodeDataName.as_view(), name='AllZipCodeDataName'),
    path('LocationAddAdminSide/', LocationAddAdminSide.as_view(), name='LocationAddAdminSide'),

    path('ApproveSupportRequest/<int:id>', ApproveSupportRequest.as_view(), name='ApproveSupportRequest'),
    path('RejectSupportRequest/<int:id>', RejectSupportRequest.as_view(), name='RejectSupportRequest'),

]