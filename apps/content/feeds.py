from django.conf import settings
from django.contrib.syndication.views import Feed    
from neighborlink.apps.content.models import *

class LatestNewsEventsFeed(Feed):
    title = "%s News and Events" % settings.SITE_NAME
    link = "/news-and-events/"
    description = "Latest news and events for %s" % settings.SITE_NAME

    def items(self):
        return NewsEvent.objects.order_by('-insert_date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

class LatestAboutPageFeed(Feed):
    title = "%s Articles" % settings.SITE_NAME
    link = "/about/"
    description = "Latest articles for %s" % settings.SITE_NAME

    def items(self):
        return AboutPage.objects.order_by('-insert_date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content