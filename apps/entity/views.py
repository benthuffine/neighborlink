from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponseRedirect

from neighborlink.apps.content.models import Page
from neighborlink.apps.content.views import page_list
from neighborlink.apps.entity.models import *

def page_detail(request, item, slug):
    return RequestContext(request, {
        'item': item,
        'slug': slug,
    })

def business_list(request):
	slug = 'businesses'
	contentpage = get_object_or_404(Page, slug__exact=slug)
	business_list = Business.objects.order_by('name')

	context = page_list(request, contentpage, business_list, slug, per_page=6)

	return render_to_response('entity/business_list.html', {}, context_instance=context)

def business_detail(request):
	business = get_object_or_404(Business, slug__exact=slug)

	context = page_detail(request, business, slug)

	return render_to_response('entity/business_detail.html', {}, context_instance=context)
