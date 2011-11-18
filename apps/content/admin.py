from django.contrib import admin
from neighborlink.apps.content.models import *

class HeroshotInline(admin.TabularInline):
    model = Heroshot
    extra = 3
    
class PageAdmin(admin.ModelAdmin):
	inlines = [
		HeroshotInline,
	]
admin.site.register(Page, PageAdmin)
