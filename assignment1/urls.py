from django.conf.urls import patterns, include, url
from django.contrib import admin
from bookmarks import views
from django.views.generic import ListView, DetailView
from bookmarks.models import Bookmark

urlpatterns = patterns('',
    url(r'^listall/$', ListView.as_view(model=Bookmark), name='listall'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^bookmark/(?P<pk>\d+)$', views.BookmarkDetail.as_view(),  name='detail'),
    url(r'^add/$', views.BookmarkCreate.as_view(), name='bookmark_add'),
    url(r'^bookmark/(?P<pk>\d+)/edit/$', views.BookmarkUpdate.as_view(),  name='bookmark_update'),
    url(r'^bookmark/(?P<pk>\d+)/delete/$', views.BookmarkDelete.as_view(),  name='bookmark_delete'),

)
