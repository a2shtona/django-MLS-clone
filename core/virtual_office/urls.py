from django.urls import path
from . import views

urlpatterns = [
    path('CreateVirtualOffice/', views.CreateVirtualOffice.as_view(), name='CreateVirtualOffice'),
    # path('CreateVirtualOffice/<slug:slug>', views.CreateVirtualOffice.as_view(), name='CreateVirtualOffice'),
    path('CreateVirtualOffice/<int:id>', views.CreateVirtualOffice.as_view(), name='CreateVirtualOffice'),
    path('GetVirtualTeamlist/<int:id>', views.GetVirtualTeamlist.as_view(), name='GetVirtualTeamlist'),
    
    path('VirtulaOfficenameShow/<int:id>', views.VirtulaOfficenameShow.as_view(), name='VirtulaOfficenameShow'),
    path('VirtualOfficePropertySend/', views.VirtualOfficePropertySend.as_view(), name='VirtualOfficePropertySend'),

    path('NotePropertyVirtualOfiice/', views.NotePropertyVirtualOfiice.as_view(), name='NotePropertyVirtualOfiice'),
    
    path('PropertyInterestinAPI/', views.PropertyInterestinAPI.as_view(), name='PropertyInterestinAPI'),
    path('PropertyInterestinAPI/<int:id>', views.PropertyInterestinAPI.as_view(), name='PropertyInterestinAPI'),
    
    path('PropertyDislikeinAPI/', views.PropertyDislikeinAPI.as_view(), name='PropertyDislikeinAPI'),
    path('PropertyDislikeinAPI/<int:id>', views.PropertyDislikeinAPI.as_view(), name='PropertyDislikeinAPI'),


    path('DeleteVirtualOfficeProperty/<int:id>', views.DeleteVirtualOfficeProperty.as_view(), name='DeleteVirtualOfficeProperty'),

    path('ShowAgentProfileOnVirtualOffice/<int:id>', views.ShowAgentProfileOnVirtualOffice.as_view(), name='ShowAgentProfileOnVirtualOffice'),

    path('VirtualOfficeTeamProfile/<int:id>', views.VirtualOfficeTeamProfile.as_view(), name='VirtualOfficeTeamProfile'),


    path('ExitVirtualOffice/', views.ExitVirtualOffice.as_view(), name='ExitVirtualOffice'),
    path('EditCustomUser/<int:id>', views.EditCustomUser.as_view(), name='EditCustomUser'),

    path('PropertyUserShowVirtualOffice/<int:id>', views.PropertyUserShowVirtualOffice.as_view(), name='PropertyUserShowVirtualOffice'),
    path('VitualOfficeUserName/<int:id>', views.VitualOfficeUserName.as_view(), name='VitualOfficeUserName'),

    path('AgentReviewGuestProfile/<int:id>', views.AgentReviewGuestProfile.as_view(), name='AgentReviewGuestProfile'),
    path('GuestReviewAgentProfile/<int:id>', views.GuestReviewAgentProfile.as_view(), name='GuestReviewAgentProfile'),

    # path('AgentSideInterestedProperty/<int:id>', views.AgentSideInterestedProperty.as_view(), name='AgentSideInterestedProperty'),
    # path('AgentSideDont_LikeProperty/<int:id>', views.AgentSideDont_LikeProperty.as_view(), name='AgentSideDont_LikeProperty'),

    path('AgnetUnExpiredListingProperty/', views.AgnetUnExpiredListingProperty.as_view(), name='AgnetUnExpiredListingProperty'),

    path('GuestAgentProfileView/<int:id>', views.GuestAgentProfileView.as_view(), name='GuestAgentProfileView'),

    path('GetTeamProfile/<int:id>', views.GetTeamProfile.as_view(), name='GetTeamProfile'),

    path('SearchTeamPerson/', views.SearchTeamPerson.as_view(), name='SearchTeamPerson'),
]