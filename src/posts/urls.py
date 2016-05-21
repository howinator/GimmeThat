from django.conf.urls import url

from . import views

urlpatterns = [

    # Homepage should maybe get re-labeled away from post list
    url(r'^$', views.post_list, name='list'),
    url(r'^create/$', views.post_create),
    url(r'^(?P<slug>[\w-]+)/$', views.post_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/delete/$', views.post_delete, name='delete'),
    url(r'^(?P<slug>[\w-]+)/edit/$', views.post_update, name='update'),
    url(r'^category/(?P<category>[\w-]+)/$',
        views.post_category, name='category'),
    url(r'grid/$', views.post_grid, name='grid'),
]
