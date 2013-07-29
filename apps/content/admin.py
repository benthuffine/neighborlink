from django.contrib import admin
from neighborlink.apps.content.models import *

def has_approval_permission(request, obj=None):
     if request.user.is_superuser or request.user.has_perm('content.can_approve_post'):
         return True
     return False

def make_approved(modeladmin, request, queryset):
    queryset.update(approved=True)
make_approved.short_description = "Mark selected entities as approved"

def make_unapproved(modeladmin, request, queryset):
    queryset.update(approved=False)
make_unapproved.short_description = "Mark selected entities as unapproved"

def is_child(obj):
    return obj.parent is None
is_child.short_description = 'Is Real Page'
is_child.boolean = True

class HeroshotInline(admin.TabularInline):
    model = Heroshot
    extra = 3
    classes = ('collapse closed',)
    
class PageAdmin(admin.ModelAdmin):
    actions = [make_approved, make_unapproved]

    inlines = [
        HeroshotInline,
    ]

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js', 
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
            '/media/js/admin/admin_list_reorder.js',
        ]

    def changelist_view(self, request, extra_context=None):
        if has_approval_permission(request):
            self.list_display = ('action_checkbox', 'title', 'slug', 'approved', is_child, 'sort_order',)
            self.list_display_links = ('title',)
            self.list_filter = ('approved', )
        else:
            self.list_display = ('title', 'sort_order',)
            self.list_display_links = ('title',)
        self.list_editable = ('sort_order',)
        return super(PageAdmin, self).changelist_view(request, extra_context)
    
    def get_form(self, request, obj=None, **kwargs):
        if has_approval_permission(request, obj):
            self.prepopulated_fields = {'slug': ('title',)}
            self.exclude = ('parent', )
        else:
            self.exclude = ('parent', 'slug', 'approved', )
        return super(PageAdmin, self).get_form(request, obj, **kwargs)

    def queryset(self, request):
        qs = super(PageAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs

        if not has_approval_permission(request):
            #   Can only see child objects
            qs = qs.filter(parent__isnull=False)

        return qs
    
    def save_model(self, request, obj, form, change):
        """
            If user can approve posts then they can edit directly, otherwise they edit shadow copy
        """
        model = self.model
        fields = ['title', 'teaser', 'content', 'sort_order',]

        obj.save()
        if has_approval_permission(request, obj):
            #   If the admin is marking as approved we copy the shadow to the parent
            if obj.parent:
                if obj.approved:
                    #   If we have a parent then we're approving the child object
                    #   Save all of the child fields to the parent
                    obj.slug = "%s-temp" % obj.parent.slug
                    for field in fields:
                        setattr(obj.parent, field, getattr(obj, field))
                    obj.parent.approved = True
                    obj.parent.save()
                    obj.approved = False
                    obj.save()
            else:
                #   if we don't have a parent then we are the parent, make sure we have a child
                field_vals = {}
                for field in fields:
                    field_vals[field] = getattr(obj, field)
                field_vals['parent'] = obj
                field_vals['approved'] = False
                field_vals['slug'] = '%s-temp' % obj.slug
                try:
                    child = model.objects.get(parent=obj)
                    for field in field_vals.keys():
                        setattr(child, field, field_vals[field])
                    child.save()
                except model.DoesNotExist:
                    child = model.objects.create(**field_vals)
        else:
            if not obj.parent:
                #   if we don't have a parent we need to create it
                field_vals = {}
                for field in fields:
                    field_vals[field] = getattr(obj, field)
                field_vals['approved'] = False
                field_vals['slug'] = '%s-temp' % obj.slug
                parent = model.objects.create(**field_vals)
                obj.parent = parent
                obj.save()
                    

    def delete_model(self, request, obj):
        #   Delete both the parent and the child
        if obj.parent:
            obj.parent.delete()
        else:
            Church.objects.filter(parent=obj).delete()
        obj.delete()
    
        
admin.site.register(Page, PageAdmin)
admin.site.register(NewsEvent, PageAdmin)
admin.site.register(AboutPage, PageAdmin)
admin.site.register(ResourcePage, PageAdmin)
admin.site.register(CommunityAssocationPage, PageAdmin)

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

