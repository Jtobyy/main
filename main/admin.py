from django.contrib import admin
 
from models import Customer, Clothe, PendingReg, Fabric, Address, Partner

def PendingRegAdmin():
    '''PendingRegAdmin'''
    list_display = ('business_name', 'brand_type')
    change_form_template = 'admin/pendingreg/change_form.html'
admin.site.register(PendingReg, PendingRegAdmin)

def PartnerAdmin():
    '''PartnerAdmin'''
    list_display = ('business_name', 'brand_type', 'legal_rep_last_name')
admin.site.register(Partner, PartnerAdmin)

admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Clothe)
admin.site.register(Fabric)
