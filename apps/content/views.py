from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponseRedirect
from datetime import datetime
from django.http import Http404

from neighborlink.apps.content.models import *

def home(request):
    contentpage = get_object_or_404(Page, slug__exact='home')
    recent_events = NewsEvent.objects.filter(start_date__lte=datetime.now(), end_date__gte=datetime.now()).order_by('start_date', 'event_start_date')[:2]

    context = RequestContext(request, {
        'contentpage': contentpage,
        'recent_events': recent_events,
    })
    
    return render_to_response('home.html', context)

def page_list(contentpage, items_list, slug):
    paginator = Paginator(items_list, 5)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        events = paginator.page(page)
    except (EmptyPage, InvalidPage):
        events = paginator.page(paginator.num_pages)

    return RequestContext(request, {
        'contentpage': contentpage,
        'page': page,
        'items': items,
        'recent_items': events_list[:10],
        'slug': slug
    })

def page_detail(item, recent_entries, slug):
    return RequestContext(request, {
        'item': item,
        'recent_entries': recent_entries,
        'slug': slug,
    })

def newsevent_list(request):
    slug = 'news-and-events'
    contentpage = get_object_or_404(Page, slug__exact=slug)
    events_list = NewsEvent.objects.filter(start_date__lte=datetime.now(), end_date__gte=datetime.now()).order_by('start_date', 'event_start_date')

    context = page_list(contentpage, events_list, slug)

    return render_to_response('page_list.html', context)

def newsevent_detail(request, slug):
    event = get_object_or_404(NewsEvent, slug__exact=slug)
    if event.start_date <= datetime.now() or event.start_date >= datetime.now():
        return Http404('Page Not Found')

    recent_entries = NewsEvent.objects.order_by('start_date', 'event_start_date')[:6]

    context = page_detail(event, recent_entries, 'news-and-events')

    return render_to_response('page_detail.html', context)

def about_list(request):
    slug = 'about'
    contentpage = get_object_or_404(Page, slug__exact=slug)
    about_list = AboutPage.objects.order_by('-insert_date')

    context = page_list(contentpage, about_list, slug)

    return render_to_response('page_list.html', context)

def about_detail(request, slug):
    about = get_object_or_404(AboutPage, slug__exact=slug)
    recent_entries = AboutPage.objects.order_by('-insert_date')[:6]

    context = RequestContext(request, {
        'article': about,
        'recent_entries': recent_entries,
        'slug': 'about',
    })

    return render_to_response('page_detail.html', context)   

def resource_list(request):
    slug = 'resources'
    contentpage = get_object_or_404(Page, slug__exact=slug)
    resource_list = ResourcePage.objects.order_by('-insert_date')

    context = page_list(contentpage, resource_list, slug)

    return render_to_response('page_list.html', context)

def resource_detail(request, slug):
    resource = get_object_or_404(ResourcePage, slug__exact=slug)
    recent_entries = ResourcePage.objects.order_by('-insert_date')[:6]

    context = RequestContext(request, {
        'article': resource,
        'recent_entries': recent_entries,
        'slug': 'resources',
    })