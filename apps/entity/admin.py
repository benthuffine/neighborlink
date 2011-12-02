from django.contrib import admin
from neighborlink.apps.entity.models import *
from django.views.decorators.csrf import csrf_protect

def has_approval_permission(request, obj=None):
     if request.user.has_perm('entity.can_approve_post'):
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

class EntityAdmin(admin.ModelAdmin):
    search_fields = ['name']

    actions = [make_approved, make_unapproved]

    def get_form(self, request, obj=None, **kwargs):
        if has_approval_permission(request, obj):
            self.prepopulated_fields = {'slug': ('name',)}
        return super(EntityAdmin, self).get_form(request, obj, **kwargs)

class TypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


#admin.site.register(Organization, EntityAdmin)
admin.site.register(BusinessType, TypeAdmin)
admin.site.register(Denomination, TypeAdmin)
admin.site.register(ServiceType, TypeAdmin)
admin.site.register(Offer)
admin.site.register(Featured)

class ChurchAdmin(EntityAdmin):
    def changelist_view(self, request, extra_context=None):
        if has_approval_permission(request):
            self.list_display = ('action_checkbox', 'name', 'slug', 'denomination', 'featurable', 'approved', is_child,)
            self.list_display_links = ('name',)
            self.list_filter = ('denomination', 'featurable', 'approved')
        else:
            self.list_display = ('name',)
            self.list_display_links = ('name',)
        return super(ChurchAdmin, self).changelist_view(request, extra_context)

    def get_form(self, request, obj=None, **kwargs):
        if has_approval_permission(request, obj):
            self.prepopulated_fields = {'slug': ('name',)}
            self.fieldsets = (
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
                }),
                ('Advanced Features', {
                    'fields': ('record_owners', 'approved', ),
                    'classes': ('collapse closed',),
                })
            )
        else:
            self.fieldsets = (
                (None, {
                    'fields': ('name', 'tagline', 'description', 'heroshot_full', 'heroshot_slim', 'denomination')
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
            #self.fieldsets[-1][-1]['fields'] = ('record_owners', 'approved',)
        return super(ChurchAdmin, self).get_form(request, obj, **kwargs)

    def queryset(self, request):
        qs = super(ChurchAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs

        if not has_approval_permission(request):
            #   Can only see child objects
            qs = qs.filter(parent__isnull=False)

        if not request.user.has_perm('entity.add_service'):
            #   If they can add church then they can edit all churches, otherwise only those they own
            qs = qs.filter(record_owners=request.user)

        return qs

    def save_model(self, request, obj, form, change):
        """
            If user can approve posts then they can edit directly, otherwise they edit shadow copy
        """
        fields = ['name', 'tagline', 'description', 'heroshot_full', 'heroshot_slim', 'denomination', 'website', 'facebook', 'twitter', 'addr1', 'addr2', 'city', 'state', 'zip', 'readable_location', 'hours', 'phone', 'email', 'founded', 'pastors']

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
                    child = Church.objects.get(parent=obj)
                    for field in field_vals.keys():
                        setattr(child, field, field_vals[field])
                except Church.DoesNotExist:
                    child = Church.objects.create(**field_vals)
                child.record_owners = obj.record_owners.all()
                child.save()
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

admin.site.register(Church, ChurchAdmin)

class ServiceAdmin(EntityAdmin):
    def changelist_view(self, request, extra_context=None):
        if has_approval_permission(request):
            self.list_display = ('action_checkbox', 'name', 'slug', 'featurable', 'approved')
            self.list_display_links = ('name',)
            self.list_filter = ('service_type', 'featurable', 'approved')
        else:
            self.list_display = ('name',)
            self.list_display_links = ('name',)
        return super(ServiceAdmin, self).changelist_view(request, extra_context)

    def get_form(self, request, obj=None, **kwargs):
        if has_approval_permission(request, obj):
            self.prepopulated_fields = {'slug': ('name',)}
            self.fieldsets = (
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
                ('Miscellaneous', {
                    'fields': ('founded', 'owners',),
                    'classes': ('collapse open',),
                }),
                ('Advanced Features', {
                    'fields': ('record_owners', 'approved',),
                    'classes': ('collapse closed',),
                })
            )
        else:
            self.fieldsets = (
                (None, {
                    'fields': ('name', 'tagline', 'description', 'heroshot_full', 'heroshot_slim', 'service_type')
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
                ('Miscellaneous', {
                    'fields': ('founded', 'owners',),
                    'classes': ('collapse open',),
                })
            )
        return super(ServiceAdmin, self).get_form(request, obj, **kwargs)
    
    def queryset(self, request):
        qs = super(ServiceAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs

        if not has_approval_permission(request):
            #   Can only see child objects
            qs = qs.filter(parent__isnull=False)

        if not request.user.has_perm('entity.add_service'):
            #   If they can add service then they can edit all services otherwise only those they own
            qs = qs.filter(record_owners=request.user)

        return qs

    def save_model(self, request, obj, form, change):
        """
            If user can approve posts then they can edit directly, otherwise they edit shadow copy
        """
        fields = ['name', 'tagline', 'description', 'heroshot_full', 'heroshot_slim', 'website', 'facebook', 'twitter', 'addr1', 'addr2', 'city', 'state', 'zip', 'readable_location', 'phone', 'email', 'founded', 'owners']

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
                    obj.parent.service_type = obj.service_type.all()
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
                    child = Service.objects.get(parent=obj)
                    for field in field_vals.keys():
                        setattr(child, field, field_vals[field])
                except Service.DoesNotExist:
                    child = Service.objects.create(**field_vals)
                child.record_owners = obj.record_owners.all()
                child.service_type = obj.service_type.all()
                child.save()
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

admin.site.register(Service, ServiceAdmin)       

class OfferInline(admin.TabularInline):
    model = Offer
    extra = 3
    classes = ('collapse closed',)

class BusinessAdmin(EntityAdmin):
    inlines = [
        OfferInline,
    ]    

    def changelist_view(self, request, extra_context=None):
        if has_approval_permission(request):
            self.list_display = ('action_checkbox', 'name', 'slug', 'business_type', 'featurable', 'approved')
            self.list_display_links = ('name',)
            self.list_filter = ('business_type', 'featurable', 'approved')
        else:
            self.list_display = ('name',)
            self.list_display_links = ('name',)
        return super(BusinessAdmin, self).changelist_view(request, extra_context)

    def get_form(self, request, obj=None, **kwargs):
        if has_approval_permission(request, obj):
            self.prepopulated_fields = {'slug': ('name',)}
            self.fieldsets = (
                (None, {
                    'fields': ('name', 'slug', 'tagline', 'description', 'featurable', 'heroshot_full', 'heroshot_slim', 'business_type')
                }),
                ('External Links', {
                    'fields': ('website', 'facebook', 'twitter', 'urbanspoon'),
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
                }),
                ('Advanced Features', {
                    'fields': ('record_owners', 'approved', ),
                    'classes': ('collapse closed',),
                })
            )
        else:
            self.fieldsets = (
                (None, {
                    'fields': ('name', 'tagline', 'description', 'heroshot_full', 'heroshot_slim', 'business_type')
                }),
                ('External Links', {
                    'fields': ('website', 'facebook', 'twitter', 'urbanspoon'),
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
        return super(BusinessAdmin, self).get_form(request, obj, **kwargs)

    def queryset(self, request):
        qs = super(BusinessAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs

        if not has_approval_permission(request):
            #   Can only see child objects
            qs = qs.filter(parent__isnull=False)

        if not request.user.has_perm('entity.add_business'):
            #   If they can add business then they can edit all businesses otherwise only those they own
            qs = qs.filter(record_owners=request.user)

        return qs

    def save_model(self, request, obj, form, change):
        """
            If user can approve posts then they can edit directly, otherwise they edit shadow copy
        """
        fields = ['name', 'tagline', 'description', 'heroshot_full', 'heroshot_slim', 'business_type', 'website', 'facebook', 'twitter', 'urbanspoon', 'addr1', 'addr2', 'city', 'state', 'zip', 'readable_location', 'hours', 'phone', 'email', 'founded', 'owners']

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
                    child = Business.objects.get(parent=obj)
                    for field in field_vals.keys():
                        setattr(child, field, field_vals[field])
                except Business.DoesNotExist:
                    child = Business.objects.create(**field_vals)
                child.record_owners = obj.record_owners.all()
                child.save()
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

admin.site.register(Business, BusinessAdmin)    