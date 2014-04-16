from django.conf.urls import patterns, include, url
from django.conf import settings
from n64.forms import QueryForm
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('n64.views',
              url(r'^$', name='home'),
              url(r'^home/$', name='home'),
			  url(r'^query/$', name='query'),
			  url(r'^watch/$', name='watch'),
			  url(r'^upload/$', name='upload'),
			  url(r'^sign_s3/$', name='sign_request'),
			  url(r'^login/$', name='login'),
			  url(r'^logout/$', name='logout'),
)
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
