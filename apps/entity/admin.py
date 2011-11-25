from django.contrib import admin
from neighborlink.apps.entity.models import *

class EntityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class TypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Church, EntityAdmin)
admin.site.register(Organization, EntityAdmin)
admin.site.register(Service, EntityAdmin)
admin.site.register(BusinessType, TypeAdmin)
admin.site.register(Denomination, TypeAdmin)
admin.site.register(ServiceType, TypeAdmin)
admin.site.register(Offer)
admin.site.register(Featured)

class OfferInline(admin.TabularInline):
    model = Offer
    extra = 3

class BusinessAdmin(EntityAdmin):
    inlines = [
        OfferInline,
    ]    

admin.site.register(Business, BusinessAdmin)    