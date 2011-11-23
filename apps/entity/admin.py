from django.contrib import admin
from neighborlink.apps.entity.models import *

class EntityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Business, EntityAdmin)
admin.site.register(Church, EntityAdmin)
admin.site.register(Organization, EntityAdmin)
admin.site.register(BusinessType)
admin.site.register(Denomination)
admin.site.register(Offer)