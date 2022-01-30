from django.contrib import admin

from .models import Customer, Tailor, Clothe

# Register your models here.
admin.site.register(Customer)
admin.site.register(Tailor)
admin.site.register(Clothe)
