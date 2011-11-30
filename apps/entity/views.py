from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponseRedirect

from neighborlink.apps.content.models import Page
from neighborlink.apps.content.views import page_list
from neighborlink.apps.entity.models import *

def page_detail(request, item, ordered_item_list, slug):
    prev_item = ordered_item_list[0]
    next_item = ordered_item_list[0]
    item_index = 1

    if prev_item == item:
        prev_item = ordered_item_list[ordered_item_list.count()-1]
  
    # Figure out where this item is situated in the list, for the prev and next links
    found = False
    for itm in ordered_item_list:
        next_item = itm
        if found:
            break
        if itm == item:
            found = True
        else:
            prev_item = itm
            item_index += 1
  
        if next_item == item:
            next_item = ordered_item_list[0]


    return RequestContext(request, {
        'item': item,
        'slug': slug,
        'prev_item': prev_item,
        'next_item': next_item,
    })

def business_list(request):
    slug = 'businesses'
    contentpage = get_object_or_404(Page, slug__exact=slug)
    business_list = Business.objects.filter(approved=True).order_by('name')

    if request.GET.get('type'):
        business_list = business_list.filter(business_type__slug__exact=request.GET.get('type'))

    context = page_list(request, contentpage, business_list, slug, per_page=6)

    return render_to_response('entity/business_list.html', {}, context_instance=context)

def business_detail(request, slug):
    business = get_object_or_404(Business, slug__exact=slug)
    business_list = Business.objects.filter(approved=True).order_by('name')

    context = page_detail(request, business, business_list, slug)

    return render_to_response('entity/business_detail.html', {}, context_instance=context)

def church_list(request):
    slug = 'churches'
    contentpage = get_object_or_404(Page, slug__exact=slug)
    church_list = Church.objects.filter(approved=True).order_by('name')

    if request.GET.get('denomination'):
        church_list = church_list.filter(denomination__slug__exact=request.GET.get('denomination'))

    context = page_list(request, contentpage, church_list, slug, per_page=6)

    return render_to_response('entity/church_list.html', {}, context_instance=context)

def church_detail(request, slug):
    church = get_object_or_404(Church, slug__exact=slug)
    church_list = Church.objects.filter(approved=True).order_by('name')

    context = page_detail(request, church, church_list, slug)

    return render_to_response('entity/church_detail.html', {}, context_instance=context)

def service_list(request):
    slug = 'services'
    contentpage = get_object_or_404(Page, slug__exact=slug)
    services_list = Service.objects.filter(approved=True).order_by('name')

    if request.GET.get('type'):
        services_list = services_list.filter(service_type__slug__exact=request.GET.get('type'))

    context = page_list(request, contentpage, services_list, slug, per_page=6)

    return render_to_response('entity/service_list.html', {}, context_instance=context)

def service_detail(request, slug):
    service = get_object_or_404(Service, slug__exact=slug)
    services_list = Service.objects.filter(approved=True).order_by('name')

    context = page_detail(request, service, services_list, slug)

    return render_to_response('entity/service_detail.html', {}, context_instance=context)
