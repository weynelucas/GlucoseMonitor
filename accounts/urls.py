from django.conf.urls import url
from accounts import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^logout$', views.logout),
    url(r'^signup$', views.signup),
    url(r'^lookup/(?P<field>[A-Za-z0-9_]+)/(?P<value>.+)', views.lookup),
]
