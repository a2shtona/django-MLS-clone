from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(UserType)
class UserType_Admin(admin.ModelAdmin):
    list_display = ['id','user','user_type']
admin.site.register(UserProfile)
admin.site.register(User_Log)
admin.site.register(User)

admin.site.register(AgentApprovedSubscriptionPlan)
admin.site.register(Nb_specality_area)
admin.site.register(SupportTickets)

admin.site.register(min_30)
admin.site.register(AccountSetting)

admin.site.register(IssueType)
admin.site.register(IssuePriority)
admin.site.register(Card)
admin.site.register(Billing)

admin.site.register(Testmodel)


@admin.register(AgentLic)
class AgentLic_Admin(admin.ModelAdmin):
    list_display = ('id','user','license_number','Full_name','first_name','last_name','is_validated','is_requested')

admin.site.register(SavedSalesPerosn)