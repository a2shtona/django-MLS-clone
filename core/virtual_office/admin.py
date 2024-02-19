from django.contrib import admin
from .models import *

admin.site.register(VirtualOffice)
admin.site.register(VirtualOfficeTeam)
admin.site.register(customer_info)
admin.site.register(VirtualOfficeProperty)
# admin.site.register(NoteOnVirtualOfficeProperty)
admin.site.register(Signed_Documnets_Custom_Info)