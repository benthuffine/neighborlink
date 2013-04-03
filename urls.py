from django.views.generic.simple import direct_to_template
from django.conf.urls.defaults import *
from django.conf import settings

handler500 = 'neighborlink.apps.content.views.server_error'

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^nlink/', include('nlink.foo.urls')),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^comments/', include('django.contrib.comments.urls')),
)

if settings.DEBUG:
  urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True }),
  )

from neighborlink.apps.content.feeds import *
urlpatterns += patterns('',
    (r'^news-and-events/feed/$', LatestNewsEventsFeed()),
    (r'^about/feed/$', LatestAboutPageFeed()),
    (r'^login/$', direct_to_template, {'template': 'login.html'}),
)

urlpatterns += patterns('neighborlink.apps.entity.views',
    (r'^businesses/$', 'business_list'),
    (r'^businesses/(?P<slug>[\w-]+)/$', 'business_detail'),
    (r'^churches/$', 'church_list'),
    (r'^churches/(?P<slug>[\w-]+)/$', 'church_detail'),
    (r'^services/$', 'service_list'),
    (r'^services/(?P<slug>[\w-]+)/$', 'service_detail'),
)

urlpatterns += patterns('neighborlink.apps.content.views',
    (r'^news-and-events/(?P<slug>[\w-]+)/$', 'newsevent_detail'),
    (r'^news-and-events/$', 'newsevent_list'),
    (r'^about/(?P<slug>[\w-]+)/$', 'about_detail'),
    (r'^about/$', 'about_list'),
    (r'^resources/(?P<slug>[\w-]+)/$', 'resource_detail'),
    (r'^resources/$', 'resource_list'),
    (r'^community-association/$', 'community_association_list'),
    (r'^community-association/(?P<slug>[\w-]+)/$', 'community_association_detail'),

    (r'^$', 'home'),
)


