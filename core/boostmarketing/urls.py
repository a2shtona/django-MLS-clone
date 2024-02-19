
from django.urls import path
from . import views

urlpatterns = [
    path('Boost-Marketing-Dashboard', views.BoostMarketingDashboard.as_view(),name='Boost-Marketing-Dashboard'),
    path('Boost-Marketing-Admin-Login/', views.BoostMarketingAdminLogin.as_view(),name='Boost-Marketing-Admin-Login'),
    
    
    path('create_Boostmarketingplan', views.create_Boostmarketingplan.as_view(),name='create_Boostmarketingplan'),
    path('Delete_Boostmarketingplan/<int:id>', views.create_Boostmarketingplan.as_view(),name='Delete_Boostmarketingplan'),
    path('Update_Boostmarketingplan/<int:id>', views.Update_BoostMarketinPlan.as_view(),name='Update_Boostmarketingplan'),
    path('boostmarketingdashboardapi/', views.BoostMarketingDashboardApi.as_view(),name='boostmarketingdashboardapi'),

    path('boostmarketingplan/', views.boostmarketingplan.as_view(),name='boostmarketingplan'),
    path('detailboostmarketingplan/<int:id>', views.detailboostmarketingplan.as_view(),name='detailboostmarketingplan'),

    path('boostmarketingplantable', views.boostmarketingplantable.as_view(),name='boostmarketingplantable'),
    path('TermsAndServices/<int:num>', views.TermsAndServices.as_view(),name='TermsAndServices'),

]