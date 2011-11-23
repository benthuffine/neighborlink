from django.contrib import admin
from neighborlink.apps.entity.models import *

class EntityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Church, EntityAdmin)
admin.site.register(Organization, EntityAdmin)
admin.site.register(BusinessType)
admin.site.register(Denomination)
admin.site.register(Offer)

class OfferInline(admin.TabularInline):
    model = Offer
    extra = 3

class BusinessAdmin(EntityAdmin):
    inlines = [
        OfferInline,
    ]    

admin.site.register(Business, BusinessAdmin)    