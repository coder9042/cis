from django.conf.urls import patterns, include, url
from cis_models.views import *
from cis_models.timetable import *
from cis_models.models import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^cis/home/$', home),
                       url(r'^cis/login/(?P<isstud>\d)/$',login),
                       url(r'^cis/login/$',login),
                       url(r'^cis/settings/$',account_settings),
                       url(r'^cis/courses/(\d)/$',course_settings),
                       url(r'^cis/rooms/(\d)/$',rooms_settings),
                       url(r'^cis/prof/(\d)/$',prof_settings),
                       url(r'^cis/tt1/(?P<batch>\d)/(?P<isstud>\d)/$',timetable,{'tt':tt1}),
                       url(r'^cis/tt1/(?P<isstud>\d)/$',timetable,{'tt':tt1}),
                       url(r'^cis/tt2/(?P<isstud>\d)/$',timetable,{'tt':tt2}),
                       url(r'^cis/tt3/(?P<isstud>\d)/$',timetable,{'tt':tt3}),
                       url(r'^cis/tt4/(?P<isstud>\d)/$',timetable,{'tt':tt4}),
                       url(r'^cis/tt1/(?P<batch>\d)$',timetable,{'tt':tt1}),
                       url(r'^cis/tt1/$',timetable,{'tt':tt1}),
                       url(r'^cis/tt2/$',timetable,{'tt':tt2}),
                       url(r'^cis/tt3/$',timetable,{'tt':tt3}),
                       url(r'^cis/tt4/$',timetable,{'tt':tt4}),
                       url(r'^cis/autogen_tt/(?P<yr>\d)/$',autogen),
                       url(r'^cis/clear/(?P<yr>\d)/$',clr),
                       url(r'^cis/mytt/$',my_timetable),
                       #url(r'^cis/tt/(?P<branch>[A-Za-z]{1,3})/$',branch_timetable),
                       url(r'^cis/gen_usrnm/$',gen_usrnm),
                       url(r'^cis/resetPass/$',resetpass),
                       url(r'^cis/filter/(?P<yr>\d)/(?P<batch>\d)/(?P<isstud>\d)$',filterTT),
                       url(r'^cis/filter/(?P<yr>\d)/(?P<batch>\d)$',filterTT),
                       url(r'^cis/filter/(?P<yr>\d)$',filterTT),
                       url(r'^cis/prof_req/$',prof_req),
                       url(r'^cis/manage_req/(?P<typ>\d)/(?P<pk>\d+)/$',manage_req),
                       url(r'^cis/manage_appoint/(?P<typ>\d)/(?P<pk>\d+)/$',manage_appoint),
                       url(r'^cis/studhome/$',studhome),
                       url(r'^cis/studlogin/$',studlogin),
                       url(r'^cis/Appoint/(\d)/$', Appointments),
                       url(r'^cis/pass/$',changePassword),
                       #url(r'^cis/docs/$', docs_view)
    # Examples:
    # url(r'^$', 'cis.views.home', name='home'),
    # url(r'^cis/', include('cis.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
