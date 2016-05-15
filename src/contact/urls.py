from django.conf.urls import url

from . import views

urlpatterns = [

    # anything coming to /contact will go to the contact us view
    # Homepage should maybe get re-labeled away from post list
    url(r'^$', views.contact_us, name='contact_us'),
]