from django.contrib import admin
from neighborlink.apps.content.models import *

class HeroshotInline(admin.TabularInline):
    model = Heroshot
    extra = 3
    
class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

    inlines = [
        HeroshotInline,
    ]

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js', 
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]
        
admin.site.register(Page, PageAdmin)
admin.site.register(NewsEvent, PageAdmin)
admin.site.register(AboutPage, PageAdmin)
admin.site.register(ResourcePage, PageAdmin)

from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld

class FlatPageAdmin(FlatPageAdminOld):
    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js', 
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]

# We have to unregister it, and then reregister
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

