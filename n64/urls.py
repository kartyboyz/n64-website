from django.conf.urls import patterns, include, url
from django.conf import settings
from n64.forms import BoxQueryForm, TextQueryForm
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('n64.views',
              url(r'^$', 'home', name='home'),
              url(r'^home/$', 'home', name='home'),
			  url(r'^query/$', 'query', name='query'),
			  url(r'^watch/$', 'watch', name='watch'),
			  url(r'^upload/$', 'upload', name='upload'),
			  url(r'^sign_s3/$', 'sign_request', name='sign_request'),
			  url(r'^login/$', 'login', name='login'),
			  url(r'^logout/$', 'logout', name='logout'),
			  url(r'^create_user/$', 'create_user', name='create_user'),
)

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
