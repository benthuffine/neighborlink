from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponseRedirect
from datetime import datetime

from neighborlink.apps.content.models import *

def home(request):
    contentpage = get_object_or_404(Page, slug__exact='home')
    recent_events = NewsEvent.objects.filter(start_date__lte=datetime.now(), end_date__gte=datetime.now()).order_by('-start_date', '-event_start_date')[2]

    context = RequestContext(request, {
        'contentpage': contentpage,
        'recent_events': recent_events,
    })
    
    return render_to_response('home.html', context)

def newsevents(request):
    contentpage = get_object_or_404(Page, slug__exact='newsevents')
    events_list = NewsEvent.objects.order_by('-start_date', '-event_start_date')

    paginator = Paginator(events_list, 5)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        events = paginator.page(page)
    except (EmptyPage, InvalidPage):
        events = paginator.page(paginator.num_pages)

    context = RequestContext(request, {
        'contentpage': contentpage,
        'page': page,
        'events': events
    })

    return render_to_response('newsevent_list.html')

  