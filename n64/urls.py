from django.conf.urls import patterns, include, url
from django.conf import settings
from n64.forms import QueryForm
from n64.views import home, query, watch, upload, sign_request
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
              url(r'^$', home), 
              url(r'^home/$', home), 
			  url(r'^query/$', query),	
			  url(r'^watch/$', watch),	
			  url(r'^upload/$', upload),	
			  url(r'^sign_s3/$', sign_request),	
			  url(r'^login/$', login),	
			  url(r'^logout/$', logout),	
)
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
