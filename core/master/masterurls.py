
from django.urls import path
from .masterviews import *
from . import adminapiviews  as apiadmin



urlpatterns = [
    path('countrymasterview',CountryMasterView.as_view(),name='countrymasterview'),
    path('countrymasterdelete/<int:id>',CountryMasterDelete.as_view(),name='countrymasterdelete'),
    path('countrymasteredit/<int:id>',CountryMasterEdit.as_view(),name='countrymasteredit'),

    path('areamasterview', AreaMasterView.as_view(), name='areamasterview'),
    path('areamasterdelete/<int:id>', DeleteAreaMaster.as_view(), name='areamasterdelete'),
    path('editareamaster/<int:id>', EditAreaMaster.as_view(), name='editareamaster'),
    
    path('couponandpromoview', CouponAndPromoView.as_view(), name='couponandpromoview'),
    path('couponandpromodelete/<int:id>', DeleteCouponAndPromo.as_view(), name='couponandpromodelete'),
    path('couponandpromoedit/<int:id>', EditCouponAndPromo.as_view(), name='couponandpromoedit'),
    
    # ZipcodeMaster Urls
    path('zipcodemasterview', ZipCodeMasterView.as_view(), name='zipcodemasterview'),
    path('zipcodemasterdelete/<int:id>', DeleteZipCodeMaster.as_view(), name='zipcodemasterdelete'),
    path('editzipcodemaster/<int:id>', EditZipCodeMaster.as_view(), name='editzipcodemaster'),

    # PetMaster Urls
    path('petmasterview', PetMasterView.as_view(), name='petmasterview'),
    path('petmasterdelete/<int:id>', DeletePetMaster.as_view(), name='petmasterdelete'),
    path('editpetmaster/<int:id>', EditPetMaster.as_view(), name='editpetmaster'),

     #HomeCardTitle
    path('homecardtitleview',HomeCardTitleView.as_view(),name='homecardtitleview'), 
    path('homecardtitledit/<int:id>',HomeCardTitleEdit.as_view(),name='homecardtitledit'),
    # path('homecardtitldelete/<int:id>',HomeCardTitleDelete.as_view(),name='homecardtitldelete'), 

    #HomeCardTitle
    path('homecardview',HomeCardView.as_view(),name='homecardview'), 
    path('homecardedit/<int:id>',HomeCardEdit.as_view(),name='homecardedit'),
    # path('homecarddelete/<int:id>',HomeCardDelete.as_view(),name='homecarddelete'), 

    # Terms
    path('terms/',TermsAdd.as_view(),name='terms'),
    path('terms/<int:id>',TermsAdd.as_view(),name='terms'),
    
    # Offers
    path('offers/',AddOffers.as_view(),name='offers'),
    path('offers/<int:id>',AddOffers.as_view(),name='offers'),
    
    # IssueType
    path('issue_type/',AddIssueType.as_view(),name='issue_type'),
    path('issue_type/<int:id>',AddIssueType.as_view(),name='issue_type'),
    
    # IssuePriority
    path('issue_priority/',AddPriorityType.as_view(),name='issue_priority'),
    path('issue_priority/<int:id>',AddPriorityType.as_view(),name='issue_priority'),

# =====================================================================================================================================
#                                                           Admin API Urls
# =====================================================================================================================================
    path('api/admin/AllTypeUser/',apiadmin.AllTypeUser.as_view(),name='api_admin_AllTypeUser'),
    path('api/admin/GuestTypeUser/',apiadmin.GuestTypeUser.as_view(),name='api_admin_GuestTypeUser'),
    path('api/admin/AgentTypeUser/',apiadmin.AgentTypeUser.as_view(),name='api_admin_AgentTypeUser'),
    path('api/admin/InvestorAndDeveloperUser/',apiadmin.InvestorAndDeveloperUser.as_view(),name='api_admin_InvestorAndDeveloperUser'),
    path('api/admin/FsbhoAndFrbhoUser/',apiadmin.FsbhoAndFrbhoUser.as_view(),name='api_admin_FsbhoAndFrbhoUser'),
    path('api/admin/ManagementUser/',apiadmin.ManagementUser.as_view(),name='api_admin_ManagementUser'),
    path('api/admin/SubAgentUser/',apiadmin.SubAgentUser.as_view(),name='api_admin_SubAgentUser'),
    path('api/admin/BoostMarketingUser/',apiadmin.BoostMarketingUser.as_view(),name='api_admin_BoostMarketingUser'),
    path('api/admin/AdvertisementUserList/',apiadmin.AdvertisementUserList.as_view(),name='AdvertisementUserList'),
    path('api/admin/InactiveUserList/',apiadmin.InactiveUserList.as_view(),name='api_admin_InactiveUserList'),
    path('api/admin/AllPendingLicenceAdminAPI/',apiadmin.AllPendingLicenceAdminAPI.as_view(),name='api_admin_AllPendingLicenceAdminAPI'),
    path('api/admin/AllNBSpecilityAdminAPI/',apiadmin.AllNBSpecilityAdminAPI.as_view(),name='api_admin_AllNBSpecilityAdminAPI'),
    path('api/admin/AllSupportTicketAdminAPI/',apiadmin.AllSupportTicketAdminAPI.as_view(),name='api_admin_AllSupportTicketAdminAPI'),
    path('api/admin/AllAgentSupportTicketAdminAPI/',apiadmin.AllAgentSupportTicketAdminAPI.as_view(),name='api_admin_AllAgentSupportTicketAdminAPI'),
    path('api/admin/AllGuestSupportTicketAdminAPI/',apiadmin.AllGuestSupportTicketAdminAPI.as_view(),name='api_admin_AllGuestSupportTicketAdminAPI'),

    # Location Admin API
    path('api/admin/CountryAdminAPI/',apiadmin.CountryAdminAPI.as_view(),name='api_admin_CountryAdminAPI'),
    path('api/admin/StateAdminAPI/',apiadmin.StateAdminAPI.as_view(),name='api_admin_StateAdminAPI'),
    path('api/admin/CityAdminAPI/',apiadmin.CityAdminAPI.as_view(),name='api_admin_CityAdminAPI'),
    path('api/admin/AreaAdminAPI/',apiadmin.AreaAdminAPI.as_view(),name='api_admin_AreaAdminAPI'),
    path('api/admin/ZipCodeAdminAPI/',apiadmin.ZipCodeAdminAPI.as_view(),name='api_admin_ZipCodeAdminAPI'),

    # Language Admin API
    path('api/admin/AllLanguageAdminAPI/',apiadmin.AllLanguageAdminAPI.as_view(),name='api_admin_AllLanguageAdminAPI'),
    
    # Term Admin API
    path('api/admin/TermsAdminAPI/',apiadmin.TermsAdminAPI.as_view(),name='api_admin_TermsAdminAPI'),
    path('api/admin/OfferAdminAPI/',apiadmin.OfferAdminAPI.as_view(),name='api_admin_OfferAdminAPI'),

    # Home Card
    # path('api/admin/HomeCardTitleAdminAPI/',apiadmin.HomeCardTitleAdminAPI.as_view(),name='api_admin_HomeCardTitleAdminAPI'),
    path('api/admin/HomeCardAdminAPI/',apiadmin.HomeCardAdminAPI.as_view(),name='api_admin_HomeCardAdminAPI'),

    path('api/admin/PropertyListingAdminAPI/',apiadmin.PropertyListingAdminAPI.as_view(),name='api_admin_PropertyListingAdminAPI'),
    path('api/admin/PropertyTypeListingAdminAPI/',apiadmin.PropertyTypeListingAdminAPI.as_view(),name='api_admin_PropertyTypeListingAdminAPI'),
    path('api/admin/MainCategoryAdminAPI/',apiadmin.MainCategoryAdminAPI.as_view(),name='api_admin_MainCategoryAdminAPI'),
    path('api/admin/Property_Sub_CategoryAdminAPI/',apiadmin.Property_Sub_CategoryAdminAPI.as_view(),name='api_admin_Property_Sub_CategoryAdminAPI'),
] 