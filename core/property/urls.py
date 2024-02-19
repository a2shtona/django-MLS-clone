from django.urls import path
from .import views, HomeApi, stackwatchviews

urlpatterns = [
    path('propertymaincategory/',views.PropertyMainCategory.as_view(),name='maincategory'),
    path('propertysubcategory/',views.PropertySubCategory.as_view(),name='propertysubcategory'),
    path('propertydetail/',views.PropertyDetail.as_view(),name='propertydetail'),
    path('propertydetail/<int:id>',views.PropertyDetail.as_view(),name='propertydetail'),
    path('propertydetail/<slug:slug>',views.PropertyDetail.as_view(),name='propertydetail'),
    path('propertyamenities/',views.PropertyAmenities.as_view(),name='propertyamenities'),
    path('propertylistingevent/',views.PropertyListingEvent.as_view(),name='propertylistingevent'),
    path('amenitiesmaster/',views.AmenitiesMaster.as_view(),name='amenitiesmaster'),


    path('AminitiesView/',views.AminitiesView.as_view(),name='AminitiesView'),
    path('PropertyTypeFilterView/',views.PropertyTypeFilterView.as_view(),name='PropertyTypeFilterView'),
    path('propertylistingtypeview/',views.Propertylisting_typeView.as_view(),name='propertylistingtypeview'),
    path('propertylisting_typeview/',views.Property_Listing_TypeView.as_view(),name='propertylisting_typeview'),
    path('seenpropertyview/',views.Seen_Property_View.as_view(),name='seenpropertyview'),
    path('loadlistingtypeaccordingtosetting/',views.LoadListingTypeAccordingToSetting.as_view(),name='loadlistingtypeaccordingtosetting'),

    # Home API urls
    # ==Residential==
    path('petfriendly/',HomeApi.Residential_property_Pet_Friendly.as_view(),name='petfriendly'),
    path('nofee/',HomeApi.Residential_property_No_Fee.as_view(),name='nofee'),
    path('residentialjustlisted/',HomeApi.Residential_property_just_listed.as_view(),name='residentialjustlisted'),
    path('salesamt/',HomeApi.luxary_sales_amount.as_view(),name='salesamt'),
    path('rentamt/',HomeApi.luxary_rent_amount.as_view(),name='rentamt'),

    path('vacation/',HomeApi.Vacation_Property.as_view(),name='vacation'),
    path('foreclouser/',HomeApi.Foreclouser_Property.as_view(),name='foreclouser'),
    path('office/',HomeApi.Ofiice_Property.as_view(),name='office'),
    path('retail/',HomeApi.Retail_Property.as_view(),name='retail'),
    path('mixed_use/',HomeApi.Mixedused_Propety.as_view(),name='mixed_use'),
    path('industrial/',HomeApi.Industrial_property.as_view(),name='industrial'),
    path('land/',HomeApi.Land_property.as_view(),name='land'),

    path('FindAreaCityState/',HomeApi.FindAreaCityState.as_view(),name='FindAreaCityState'),


    # ==Commercial==
    # path('Commercial_Property/',HomeApi.Commercial_Property.as_view(),name='Commercial_Property'),
    path('commercialjustlisted/',HomeApi.Commercial_property_just_listed.as_view(),name='commercialjustlisted'),

    # ==Nearest property==
    path('Residential_Nearest_property/',HomeApi.Residential_Nearest_property.as_view(),name='Residential_Nearest_property'),
    path('Commercial_Nearest_property/',HomeApi.Commercial_Nearest_property.as_view(),name='Commercial_Nearest_property'),
    path('Recidential_check_property/',HomeApi.Recidential_check_property.as_view(),name='Recidential_check_property'),
    path('Commercial_check_property/',HomeApi.Commercial_check_property.as_view(),name='Commercial_check_property'),

    path('propertylistingaccordingtopropertylistingtype/',views.PropertyListingAccordingToPropertyListingType.as_view(),name='propertylistingaccordingtopropertylistingtype'),
    path('propertylistingaccordingtopropertylistingtype/<int:id>',views.PropertyListingAccordingToPropertyListingType.as_view(),name='propertylistingaccordingtopropertylistingtype'),

    path('propertymaicategorytypehomeview/',views.Property_Main_Category_Type_HomeView.as_view(),name='propertymaicategorytypehomeview'),
    path('propertysubcategorytypehomeview/',views.Property_Sub_Category_Type_HomeView.as_view(),name='propertysubcategorytypehomeview'),

    path('savealllisting/',views.SaveAllListing.as_view(),name='savealllisting'),
    path('deleteallsavelisting/',views.DeleteAllSaveListing.as_view(),name='deleteallsavelisting'),

    # Filter
    path('filter_property_residential/',HomeApi.PropertyRescidentialFilter.as_view(),name='filter_property_residential'),
    path('filter_property_commercial/',HomeApi.PropertyCommercialFilter.as_view(),name='filter_property_commercial'),
    
    path('Invitation_link/',views.InvitationView.as_view(), name='Invitation_link'),
    path('BluckInvitation_View/',views.BluckInvitationView.as_view(), name='BluckInvitation_View'),
    # path('accept_invitation/',views.Accept_invitation.as_view(), name='accept_invitation'),
    path('agentregister/',views.RegistrationAgentAPI.as_view(), name='agentregister'),
    path('teammerberprofile/<slug:slug>',views.TeamMemberProfile.as_view(), name='teammerberprofile'),
    path('UpdateTeamMember/<int:id>',views.UpdateTeamMember.as_view(), name='UpdateTeamMember'),
    path('RemoveTeamMember/<int:id>',views.RemoveTeamMember.as_view(), name='RemoveTeamMember'),


    # StackwatchAPI
    path('daywise/',stackwatchviews.Daywise.as_view(),name='daywise'),
    path('weekwise/',stackwatchviews.Weekwise.as_view(),name='weekwise'),
    path('monthwise/',stackwatchviews.Monthwise.as_view(),name='monthwise'),
    path('coustomdate/',stackwatchviews.Coustomize_date.as_view(),name='coustomdate'),


    path('deleteproperty/',views.DeleteProperty.as_view(),name='deleteproperty'),


    path('ispropertyopen/',views.Update_is_property_open.as_view(),name='ispropertyopen'),
    path('ispropertyopen/<int:id>',views.Update_is_property_open.as_view(),name='ispropertyopen'),
    path('currentlisting/<slug:slug>',views.CurrentlistingProperty.as_view(),name='currentlisting'),
    path('closelisting/<slug:slug>',views.CloselistingProperty.as_view(),name='closelisting'),

    path('currentlistingcount/<slug:slug>',views.CurrentlistingPropertycount.as_view(),name='currentlistingcount'),
    path('closelistingcount/<slug:slug>',views.CloselistingPropertycount.as_view(),name='closelistingcount'),
    path('totallistingcount/<slug:slug>',views.TotallistingPropertycount.as_view(),name='totallistingcount'),

    path('Update_is_property_expired/',views.Update_is_property_expired.as_view(),name='Update_is_property_expired'),
    path('ExpiredListingProperty/<int:id>',views.ExpiredListingProperty.as_view(),name='ExpiredListingProperty'),
    # path('UnExpiredListingProperty/<int:id>',views.UnExpiredListingProperty.as_view(),name='UnExpiredListingProperty'),
    path('UnExpiredListingProperty/',views.UnExpiredListingProperty.as_view(),name='UnExpiredListingProperty'),
    path('AgentDashboardProperty/',views.AgentDashboardProperty.as_view(),name='AgentDashboardProperty'),
    

    path('GetPropertyBasedOnLocation/<int:id>',views.GetPropertyBasedOnLocation.as_view(),name='GetPropertyBasedOnLocation'),
    path('GetPropertyBasedOnLocation/',views.GetPropertyBasedOnLocation.as_view(),name='GetPropertyBasedOnLocation'),



    path('propertytypefilterview/',views.PropertyTypeFilterView.as_view(),name='propertytypefilterview'),

    path('filtersavesearch/',views.Filter_Save_Search.as_view(),name='filtersavesearch'),
    path('filtersavesearch/<int:id>',views.Filter_Save_Search.as_view(),name='filtersavesearch'),
    path('filtersavesearchget/<int:id>',views.filter_save_serach_get.as_view(),name='filtersavesearchget'),
    # path('Filter/<int:id>',views.Filter.as_view(),name='Filter'),


    path('teammembershow/<slug:slug>',views.TeamMemberShow.as_view(),name='teammembershow'),
    path('contact_now/',views.Contact_Now.as_view(),name='contact_now'),

    # path('filtersavelistingforleisure/',views.filter_save_listing_for_Leisure.as_view(),name='filtersavelistingforleisure'),

    #for Home Card Title API
    path('homecardtitle/',HomeApi.Home_Card_Title.as_view(),name='homecardtitle'),

    #for Home Card  API
    path('homecard/',HomeApi.Home_Card.as_view(),name='homecard'),


    path('search/',HomeApi.search_filter.as_view(),name='search'),
    path('neighbourhood/',views.Property_Neighbourhood.as_view(),name='neighbourhood'),
    # path('DefaultPropertyShow/<int:id>',views.DefaultPropertyShow.as_view(),name='DefaultPropertyShow'),

    path('getpropertydetail/',views.GetPropertyDetail.as_view(),name='getpropertydetail'),
    path('getpropertyamenities/',views.GetPropertyAmenities.as_view(),name='getpropertyamenities'),
    path('getpropertyimage/',views.GetPropertyImage.as_view(),name='getpropertyimage'),
    path('getpropertyspaces/',views.GetPropertySpaces.as_view(),name='getpropertyspaces'),
    path('GetNeibourhoodBasedOnLocation/',views.GetNeibourhoodBasedOnLocation.as_view(),name='GetNeibourhoodBasedOnLocation'),
    path('Get30min/',views.Get30min.as_view(),name='Get30min'),
    path('GetlistingDate/',views.GetlistingDate.as_view(),name='GetlistingDate'),
    path('Filter/<int:id>',views.Filter.as_view(),name='Filter'),

    path('Rating_Review/<int:id>',views.Rating_Review.as_view(),name='Rating_Review'),
    path('ShowAgentMemeber/<int:id>',views.ShowAgentMemeber.as_view(),name='ShowAgentMemeber'),
    path('RemoveNoLongerAvaliable/<int:id>',views.RemoveNoLongerAvaliable.as_view(),name='RemoveNoLongerAvaliable'),
    path('UpdateSaveListing/',views.UpdateSaveListing.as_view(),name='UpdateSaveListing'),
    # path('GetTerms/',views.GetTerms.as_view(),name='GetTerms'),
    path('GetTermsOffer/',views.GetTermsOffer.as_view(),name='GetTermsOffer'),


    path('ReafreshAPI/',views.ReafreshAPI.as_view(),name='ReafreshAPI'),
    path('ListingSlugid/<int:id>',views.ListingSlugid.as_view(),name='ListingSlugid'),
    path('RemoveTeam/<int:id>',views.RemoveTeam.as_view(),name='RemoveTeam'),


    path('StateDashboard/',views.StateDashboard.as_view(),name='StateDashboard'),
    path('CityDependentState/',views.CityDependentState.as_view(),name='CityDependentState'),
    path('AreaDependentCity/',views.AreaDependentCity.as_view(),name='AreaDependentCity'),
    path('ZipCodeDependeOnCityArea/',views.ZipCodeDependeOnCityArea.as_view(),name='ZipCodeDependeOnCityArea'),

    path('DocumentsAPI/', views.DocumentsAPI.as_view(), name='DocumentsAPI'),
    path('DocumentShareStatusAPI/', views.DocumentShareStatusAPI.as_view(), name='DocumentShareStatusAPI'),
    path('ShareDocumentAPI/', views.ShareDocumentAPI.as_view(), name='ShareDocumentAPI'),
    path('SignDocumentAPI/', views.SignDocumentAPI.as_view(), name='SignDocumentAPI'),    
    path('DocumentOrderAPI/', views.DocumentOrderAPI.as_view(), name='DocumentOrderAPI'),
    path('DocTitleRenameAPI/', views.DocTitleRenameAPI.as_view(), name='DocTitleRenameAPI')
]