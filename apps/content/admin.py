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

