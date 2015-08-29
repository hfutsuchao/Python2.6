from django.conf.urls import patterns, include, url
from views import *
from books import views
import contact

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^hello/$', hello),
    (r'^userinfo/$', views.displayMeta),
    (r'^search/$', views.search),
    (r'^contact/$', contact.views.contact),
    #(r'^stat/(.*)/(.*)/(\d{0,3})/$', stat),
    #(r'^uvpv/(.*)/(.*)/(.*)/$', uvPVPub),
    #(r'^sources/(.*)/$', getCitysSources),
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
