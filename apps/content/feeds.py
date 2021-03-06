from django.conf import settings
from django.contrib.syndication.views import Feed    
from neighborlink.apps.content.models import *

import datetime

class LatestNewsEventsFeed(Feed):
    title = "%s News and Events" % settings.SITE_NAME
    link = "/news-and-events/"
    description = "Latest news and events for %s" % settings.SITE_NAME

    def items(self):
        return NewsEvent.objects.filter(start_date__lte=datetime.datetime.now(), end_date__gte=datetime.datetime.now(), approved=True).order_by('-event_start_date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_pubdate(self, item):
        return datetime.datetime.combine(item.insert_date, datetime.time())

class LatestAboutPageFeed(Feed):
    title = "%s Articles" % settings.SITE_NAME
    link = "/about/"
    description = "Latest articles for %s" % settings.SITE_NAME

    def items(self):
        return AboutPage.objects.filter(approved=True).order_by('-insert_date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_pubdate(self, item):
        return datetime.datetime.combine(item.insert_date, datetime.time())