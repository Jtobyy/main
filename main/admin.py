from django.contrib import admin

from .models import Customer, Tailor, Clothe, Seller, PendingTailorReg, PendingSellerReg

# Register your models here.
admin.site.register(Customer)
admin.site.register(Tailor)
admin.site.register(Clothe)
admin.site.register(Seller)
admin.site.register(PendingTailorReg)
admin.site.register(PendingSellerReg)
