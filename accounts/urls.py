from django.conf.urls import url
from accounts import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^accounts/login', views.login),
    url(r'^accounts/logout', views.logout),
    url(r'^accounts/signup', views.signup),
    url(r'^accounts/set_password', views.set_password),
    url(r'^accounts/lookup/(?P<field>[A-Za-z0-9_]+)/(?P<value>.+)', views.lookup),
    url(r'^accounts/check_password/(?P<password>.+)', views.check_password),
]
