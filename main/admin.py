from django.contrib import admin

from .models import Customer, Cloth, PendingReg, SewedClothOrder
from .models import Fabric, Address, Partner, FabricOrder, CustomMadeOrder
from .models import FabricSeller, CustomMadeSeller, Tailor
from .models import MaleCustomerMeasurement, FemaleCustomerMeasurement

# Register your models here.
class PendingRegAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'brand_type')
    change_form_template = 'admin/pendingreg/change_form.html'
admin.site.register(PendingReg, PendingRegAdmin)

class PartnerAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'brand_type', 'legal_rep_last_name')
admin.site.register(Partner, PartnerAdmin)

class FabricOrderAdmin(admin.ModelAdmin):
    list_display = ('order_item', 'order_customer', 'order_status')
admin.site.register(FabricOrder, FabricOrderAdmin)

class FabricAdmin(admin.ModelAdmin):
    list_display = ('label', 'type', 'partner')
admin.site.register(Fabric, FabricAdmin)

admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(FabricSeller)
admin.site.register(Tailor)
admin.site.register(Cloth)
admin.site.register(CustomMadeSeller)
admin.site.register(MaleCustomerMeasurement)
admin.site.register(FemaleCustomerMeasurement)
admin.site.register(CustomMadeOrder)
admin.site.register(SewedClothOrder)
