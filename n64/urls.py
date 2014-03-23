from django.conf.urls import patterns, include, url
from django.conf import settings
from n64.forms import QueryForm

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('n64.views',
              url(r'^$', home), 
			  url(r'^query/$', query),	
			  url(r'^time/$', current_datetime),	
			  url(r'^time/(\d{1,2})/$', hours_ahead),	
                          url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)
    # Examples:
    # url(r'^n64/', include('n64.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
