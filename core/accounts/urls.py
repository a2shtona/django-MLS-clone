from django.urls import path
from .import views
from . import accountviews as aview
from . import profilepasswordviews as bview

urlpatterns = [
    path('register/',views.UserRegistrationsView.as_view(),name='register'),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('logout/',views.UserLogoutView.as_view(),name='logout'),
    path('profile/<int:id>',views.UserProfileView.as_view(),name='profile'),
    path('profile/',views.UserProfileView.as_view(),name='profile'),
    path('forgetpassword/',views.ForgetPassword.as_view(),name='forgetpassword'),
    path('changepassword/',views.UserChangePasswordView.as_view(),name='changepassword'),
    path('profileimage/',views.ChangeProfilePictureView.as_view(),name="profileimage"),
    path('email-verify/', views.VerifyEmail.as_view(), name="email-verify"),
    path('reset-password/',views.ResetPassword.as_view(), name="reset-password"),
    path('guest-User-Profile/', views.GuestUserProfile.as_view(), name="guest-User-Profile"),
    path('guest-User-Profile/<int:id>', views.GuestUserProfile.as_view(), name="guest-User-Profile"),
    path('account-setting/', aview.AccountSettingView.as_view(), name="account-setting"),
    path('account-setting/<int:id>', aview.AccountSettingView.as_view(), name="account-setting"),
    path('guest_user_save_listing/', aview.Guest_Users_Save_Listing_View.as_view(), name="guest_user_save_listing"),
    path('guest_user_save_listing/<int:id>', aview.Guest_Users_Save_Listing_View.as_view(), name="guest_user_save_listing"),
    path('delete_user_account/<int:id>', aview.Delete_User_account.as_view(), name="delete_user_account"),
    path('suspend_user_account/<int:id>', aview.Suspend_User_account.as_view(), name="suspend_user_account"),
    path('agentuserprofile/', aview.AgentUserProfile.as_view(), name="agentuserprofile"),
    path('agentuserprofile/<slug:slug>', aview.AgentUserProfile.as_view(), name="agentuserprofile"),
    path('Teamemeberlanguageandcity/<slug:slug>', aview.Teamemeberlanguageandcity.as_view(), name="Teamemeberlanguageandcity"),
    path('agentapprovedsubscriptionplanview/', views.AgentApprovedSubscriptionPlanView.as_view(), name="agentapprovedsubscriptionplanview"),
    path('agentapprovedsubscriptionplanchoices/', views.AgentApprovedSubscriptionplanchoices.as_view(), name="agentapprovedsubscriptionplanchoices"),
    path('agentdashboardwithlistingtype/', views.AgentDashboardWithListingType.as_view(), name="agentdashboardwithlistingtype"),
   
    path('brokerageLic/', aview.Brokerage_name_license.as_view(), name="brokerageLic"),
    path('brokerageLic/<slug:slug>', aview.Brokerage_name_license.as_view(), name="brokerageLic"),
    path('socialmedialink/', aview.SocilMediaLink.as_view(), name="socialmedialink"),
    path('socialmedialink/<slug:slug>', aview.SocilMediaLink.as_view(), name="socialmedialink"),
    path('createteam/', aview.Create_Team_Name.as_view(), name="createteam"),
    path('createteam/<int:id>', aview.Create_Team_Name.as_view(), name="createteam"),

    path('neighborhoodspecialisareasaved/', views.Neighborhood_Specialist_Area_Saved.as_view(), name="neighborhoodspecialisareasaved"),
    path('neighborhoodspecialisareasaved/<slug:slug>', views.Neighborhood_Specialist_Area_Saved.as_view(), name="neighborhoodspecialisareasaved"),
    path('supportticketview/', views.SupportTicketView.as_view(), name="supportticketview"),
    path('supportticketview/<int:id>', views.SupportTicketView.as_view(), name="supportticketview"),
    path('agentlicview/<int:id>', views.AgentLicView.as_view(), name="agentlicview"),
    
    # path('adminapprovedagentsubscriptionplan/', views.AdminApprovedAgentSubscriptionPlan.as_view(), name="adminapprovedagentsubscriptionplan"),

    path('profilepassword/', bview.Profile_Password.as_view(), name="profilepassword"),
    path('checkpassword/', bview.CheckUserProfilePassword.as_view(), name="checkpassword"),
    path('checkprofilepassword/', bview.Checkprofilepassword.as_view(), name="checkprofilepassword"),
    path('RemovePropefilePassword/', bview.RemovePropefilePassword.as_view(), name="RemovePropefilePassword"),
    path('ForgetProfilePassword/', bview.ForgetProfilePassword.as_view(), name="ForgetProfilePassword"),
    path('ResetProfilePassword/', bview.ResetProfilePassword.as_view(), name="ResetProfilePassword"),

    path('card_create/', views.card_create.as_view(), name="card_create"),
    path('card_create/<int:id>', views.card_create.as_view(), name="card_create"),


    path('billing/', views.billing.as_view(), name="billing"),
    path('billing/<int:id>', views.billing.as_view(), name="billing"),

    path('SocialMedia_Login_Signup_Api/', views.SocialMedia_Login_Signup_Api.as_view(), name="SocialMedia_Login_Signup_Api"),

    path('min_30_view/', aview.min_30_view.as_view(), name="min_30_view"),
    path('min_30_view/<slug:slug>', aview.min_30_view.as_view(), name="min_30_view"),
    
    
    path('plan_and_billing/<int:id>', aview.plan_and_billing.as_view(), name="plan_and_billing"),
    
    path('plan_and_billing/', aview.plan_and_billing.as_view(), name="plan_and_billing"),
    path('AddIssuePriorityType/', aview.AddIssuePriorityType.as_view(), name="AddIssuePriorityType"),

    
    path('ActivateDeactivate30Min/<slug:slug>', views.ActivateDeactivate30Min.as_view(), name="ActivateDeactivate30Min"),

        
    path('SalesPersonSearch/',views.SalesPersonSearch.as_view(),name='SalesPersonSearch'),
    path('SalespersonSavedbyGuest/',views.SalespersonSavedbyGuest.as_view(),name='SalespersonSavedbyGuest'),
    path('SalespersonSavedbyGuest/<int:id>',views.SalespersonSavedbyGuest.as_view(),name='SalespersonSavedbyGuest'),
    path('DeleteSavedSalesPerson/',views.DeleteSavedSalesPerson.as_view(),name='DeleteSavedSalesPerson'),

    path('LandloardProfileSetting/',views.LandloardProfileSetting.as_view(),name='LandloardProfileSetting'),
    path('LandloardProfileSetting/<slug:slug>',views.LandloardProfileSetting.as_view(),name='LandloardProfileSetting'),
]