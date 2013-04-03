from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponseRedirect
from datetime import datetime
from django.conf import settings
from django import http
from django.http import Http404

from neighborlink.apps.content.models import *

def server_error(request, template_name='500.html'):
    """
    500 error handler.

    Templates: `500.html`
    Context:
        MEDIA_URL
            Path of static media (e.g. "media.example.org")
    """
    t = loader.get_template(template_name) # You need to create a 500.html template.

    return http.HttpResponseServerError(t.render(Context({
        'MEDIA_URL': settings.MEDIA_URL
    })))   

def home(request):
    from neighborlink.apps.entity.models import Featured, Business

    contentpage = get_object_or_404(Page, slug__exact='home')
    recent_events = NewsEvent.objects.filter(start_date__lte=datetime.now(), end_date__gte=datetime.now(), approved=True).order_by('-start_date', '-event_start_date')[:2]

    featured_business = Featured.objects.filter(entity__approved=True).order_by('-date_featured')
    if not featured_business:
        #   Pick a random featurable business
        featured_business = Business.objects.filter(featurable=True, approved=True).order_by('?')[0]

    context = RequestContext(request, {
        'contentpage': contentpage,
        'recent_events': recent_events,
        'featured_business': featured_business
    })
    
    return render_to_response('content/home.html', {}, context_instance=context)

def page_list(request, contentpage, items_list, slug, per_page=5):
    paginator = Paginator(items_list, per_page)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        items = paginator.page(page)
    except (EmptyPage, InvalidPage):
        items = paginator.page(paginator.num_pages)

    return RequestContext(request, {
        'contentpage': contentpage,
        'page': page,
        'items': items,
        'recent_items': items_list[:10],
        'slug': slug,
    })

def page_detail(request, item, recent_entries, slug):
    return RequestContext(request, {
        'item': item,
        'recent_entries': recent_entries,
        'slug': slug,
    })

def newsevent_list(request):
    slug = 'news-and-events'
    contentpage = get_object_or_404(Page, slug__exact=slug, approved=True)
    events_list = NewsEvent.objects.filter(start_date__lte=datetime.now(), end_date__gte=datetime.now(), approved=True).order_by('sort_order', '-start_date', '-event_start_date')

    context = page_list(request, contentpage, events_list, slug)

    return render_to_response('content/newsevent_list.html', {}, context_instance=context)

def newsevent_detail(request, slug):
    event = get_object_or_404(NewsEvent, slug__exact=slug)
    if event.start_date > datetime.now().date() or event.end_date < datetime.now().date():
        raise Http404('Page Not Found')

    recent_entries = NewsEvent.objects.filter(start_date__lte=datetime.now(), end_date__gte=datetime.now(), approved=True).exclude(slug__exact=slug).order_by('start_date', 'event_start_date')[:6]

    context = page_detail(request, event, recent_entries, 'news-and-events')

    return render_to_response('content/newsevent_detail.html', {}, context_instance=context)

def about_list(request):
    slug = 'about'
    contentpage = get_object_or_404(Page, slug__exact=slug, approved=True)
    about_list = AboutPage.objects.filter(approved=True).order_by('sort_order')

    context = page_list(request, contentpage, about_list, slug)

    return render_to_response('content/about_list.html', {}, context_instance=context)

def about_detail(request, slug):
    about = get_object_or_404(AboutPage, slug__exact=slug)
    recent_entries = AboutPage.objects.filter(approved=True).exclude(slug__exact=slug).order_by('sort_order')[:6]

    context = page_detail(request, about, recent_entries, 'about')

    return render_to_response('content/about_detail.html', {}, context_instance=context)   

def resource_list(request):
    slug = 'resources'
    contentpage = get_object_or_404(Page, slug__exact=slug, approved=True)
    resource_list = ResourcePage.objects.filter(approved=True).order_by('sort_order')

    context = page_list(request, contentpage, resource_list, slug)

    return render_to_response('content/resource_list.html', {}, context_instance=context)

def resource_detail(request, slug):
    resource = get_object_or_404(ResourcePage, slug__exact=slug)
    recent_entries = ResourcePage.objects.filter(approved=True).exclude(slug__exact=slug).order_by('sort_order')[:6]

    context = page_detail(request, resource, recent_entries, 'resources')

    return render_to_response('content/resource_detail.html', {}, context_instance=context)

def community_association_list(request):
    slug = 'community-association'
    contentpage = get_object_or_404(Page, slug__exact=slug, approved=True)
    community_association_list = CommunityAssocationPage.objects.filter(approved=True).order_by('sort_order')

    context = page_list(request, contentpage, community_association_list, slug)

    return render_to_response('content/community_association_list.html', {}, context_instance=context)

def community_association_detail(request, slug):
    community_association_page = get_object_or_404(CommunityAssocationPage, slug__exact=slug)
    recent_entries = CommunityAssocationPage.objects.filter(approved=True).exclude(slug__exact=slug).order_by('sort_order')[:6]

    context = page_detail(request, community_association_page, recent_entries, 'community-association')

    return render_to_response('content/community_association_detail.html', {}, context_instance=context)
    