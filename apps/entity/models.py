from django import forms
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Entity(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=255)
    tagline = models.CharField(max_length=1024, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    website = models.URLField(verify_exists=True, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    facebook = models.URLField(verify_exists=True, null=True, blank=True)
    twitter = models.URLField(verify_exists=True, null=True, blank=True)
    addr1 = models.CharField(max_length=512, null=True, blank=True)
    addr2 = models.CharField(max_length=512, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    phone = models.CharField(max_length=16, null=True, blank=True)
    zip = models.CharField(max_length=10, null=True, blank=True)
    founded = models.CharField(max_length=128, null=True, blank=True)
    featurable = models.BooleanField(default=False)
    readable_location = models.CharField(max_length=2046, null=True, blank=True)
    record_owners = models.ManyToManyField(User, null=True, blank=True)
    heroshot_full = models.ImageField(upload_to='ext/heroshots/entity', null=True, blank=True)
    heroshot_slim = models.ImageField(upload_to='ext/heroshots/entity', null=True, blank=True)
    approved = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_address(self, single_line=True):
        joiner = single_line and ' ' or '<br>'
        
        addr = [self.addr1,]
        if self.addr2:
            addr.append("%s," % self.addr2)
        else:
            addr[0] = "%s," % addr[0]
        
        if self.city:
            addr.append("%s," % self.city)
        
        if self.state:
            addr.append(self.state)
        
        if self.zip:
            addr.append(self.zip)

        return joiner.join(addr)

    def get_single_line_address(self):
        return self.get_address(single_line=True)
    single_line_address = property(get_single_line_address)

    def get_multi_line_address(self):
        return self.get_address(single_line=False)
    multi_line_address = property(get_multi_line_address)

    def get_google_maps_url(self):
        return self.addr1 and 'http://maps.google.com/maps?q= %s' % self.get_address() or ''
    google_maps_url = property(get_google_maps_url)

    class Meta:
        ordering = ["name"]
        permissions = (
            ("can_approve_post", "Can approve post"),
        )


class BusinessType(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=255)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/businesses/?type=%s' % self.slug

    class Meta:
        ordering = ["name"]

class Denomination(models.Model):
    name = models.CharField(max_length=1024)
    slug = models.SlugField(max_length=255)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/churches/?denomination=%s' % self.slug

    class Meta:
        ordering = ["name"]
        
class ServiceType(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=255)
    
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/services/?type=%s' % self.slug

    class Meta:
        ordering = ["name"]

class Business(Entity):
    hours = models.CharField(max_length=1024, null=True, blank=True)
    business_type = models.ForeignKey(BusinessType)
    features = models.CharField(max_length=1024, null=True, blank=True)
    owners = models.CharField(max_length=1024, null=True, blank=True)
    urbanspoon = models.URLField(verify_exists=True, null=True, blank=True)

    def get_absolute_url(self):
        return '/businesses/%s/' % self.slug

    def get_current_offers(self):
        return self.offer_set.filter(start_date__lte=datetime.now(), end_date__gte=datetime.now())
    current_offers = property(get_current_offers)

    class Meta:
        verbose_name_plural = 'Businesses'

class Church(Entity):
    hours = models.CharField(max_length=1024, null=True, blank=True)
    denomination = models.ForeignKey(Denomination)
    pastors = models.CharField(max_length=1024, null=True, blank=True)

    def get_absolute_url(self):
        return '/churches/%s/' % self.slug

    class Meta:
        verbose_name_plural = 'Churches'

class Service(Entity):
    service_type = models.ManyToManyField(ServiceType)
    owners = models.CharField(max_length=1024, null=True, blank=True)

    def get_absolute_url(self):
        return '/services/%s/' % self.slug

class Organization(Entity):
    pass

    def get_absolute_url(self):
        return '/organizations/%s/' % self.slug

class Offer(models.Model):
    name = models.CharField(max_length=512)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    business = models.ForeignKey(Business) 

    def __unicode__(self):
        return self.name

class Featured(models.Model):
    entity = models.ForeignKey(Entity)
    date_featured = models.DateField()

    def __unicode__(self):
        return self.entity.name

    def clean_entity(self):
        if not self.entity.featurable:
            raise forms.ValidationError('The entity is not featureable.')
        return self.cleaned_data['entity']
