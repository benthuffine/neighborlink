from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponseRedirect

from neighborlink.apps.content.models import *

def home(request):
    contentpage = get_object_or_404(Page, slug__exact='home')

    context = RequestContext(request, {
        'contentpage': contentpage,
    })
    
    return render_to_response('home.html', context)