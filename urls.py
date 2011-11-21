from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^nlink/', include('nlink.foo.urls')),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    
)

if settings.DEBUG:
  urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True }),
  )

from neighborlink.apps.content.feeds import *
urlpatterns += patterns('',
    (r'^news-and-events/feed/$', LatestNewsEventsFeed()),
    (r'^about/feed/$', LatestAboutPageFeed()),
)

urlpatterns += patterns('neighborlink.apps.content.views',
    (r'^news-and-events/(?P<slug>[\w-]+)/$', 'newsevent_detail'),
    (r'^news-and-events/$', 'newsevent_list'),
    (r'^about/(?P<slug>[\w-]+)/$', 'about_detail'),
    (r'^about/$', 'about_list'),
    (r'^resources/(?P<slug>[\w-]+)/$', 'resource_detail'),
    (r'^resources/$', 'resource_list'),
    (r'^$', 'home'),
)


