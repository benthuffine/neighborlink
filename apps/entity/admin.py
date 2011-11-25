from django.contrib import admin
from neighborlink.apps.entity.models import *

class EntityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'tagline', 'description', 'featurable', 'heroshot_full', 'heroshot_slim')
        }),
        ('External Links', {
            'fields': ('website', 'facebook', 'twitter'),
            'classes': ('collapse open',),
        }),
        ('Address Info', {
            'fields': ('addr1', 'addr2', 'city', 'state', 'zip', 'readable_location'),
            'classes': ('collapse open',),
        }),
        ('Contact Info', {
            'fields': ('phone', 'email'),
            'classes': ('collapse open',),
        }),
        (None, {
            'fields': ('founded',)
        })
    )

    search_fields = ['name']

class TypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Organization, EntityAdmin)
admin.site.register(BusinessType, TypeAdmin)
admin.site.register(Denomination, TypeAdmin)
admin.site.register(ServiceType, TypeAdmin)
admin.site.register(Offer)
admin.site.register(Featured)

class ChurchAdmin(EntityAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'tagline', 'description', 'featurable', 'heroshot_full', 'heroshot_slim', 'denomination')
        }),
        ('External Links', {
            'fields': ('website', 'facebook', 'twitter'),
            'classes': ('collapse open',),
        }),
        ('Address Info', {
            'fields': ('addr1', 'addr2', 'city', 'state', 'zip', 'readable_location'),
            'classes': ('collapse open',),
        }),
        ('Contact Info', {
            'fields': ('hours', 'phone', 'email'),
            'classes': ('collapse open',),
        }),
        ('Miscellaneous', {
            'fields': ('founded', 'pastors'),
            'classes': ('collapse open',),
        })
    )

    list_filter = ('denomination', 'featurable')

admin.site.register(Church, ChurchAdmin)

class ServiceAdmin(EntityAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'tagline', 'description', 'featurable', 'heroshot_full', 'heroshot_slim', 'service_type')
        }),
        ('External Links', {
            'fields': ('website', 'facebook', 'twitter'),
            'classes': ('collapse open',),
        }),
        ('Address Info', {
            'fields': ('addr1', 'addr2', 'city', 'state', 'zip', 'readable_location'),
            'classes': ('collapse open',),
        }),
        ('Contact Info', {
            'fields': ('phone', 'email'),
            'classes': ('collapse open',),
        }),
        (None, {
            'fields': ('founded',)
        })
    )

    list_filter = ('service_type', 'featurable')
       
admin.site.register(Service, ServiceAdmin)       

class OfferInline(admin.TabularInline):
    model = Offer
    extra = 3

class BusinessAdmin(EntityAdmin):
    inlines = [
        OfferInline,
    ]    

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'tagline', 'description', 'featurable', 'heroshot_full', 'heroshot_slim', 'business_type')
        }),
        ('External Links', {
            'fields': ('website', 'facebook', 'twitter'),
            'classes': ('collapse open',),
        }),
        ('Address Info', {
            'fields': ('addr1', 'addr2', 'city', 'state', 'zip', 'readable_location'),
            'classes': ('collapse open',),
        }),
        ('Contact Info', {
            'fields': ('hours', 'phone', 'email'),
            'classes': ('collapse open',),
        }),
        ('Miscellaneous', {
            'fields': ('founded', 'owners', 'features'),
            'classes': ('collapse open',),
        })
    )

    list_filter = ('business_type', 'featurable')

admin.site.register(Business, BusinessAdmin)    