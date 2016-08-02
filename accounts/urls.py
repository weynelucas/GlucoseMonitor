from django.conf.urls import url
from accounts import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^logout$', views.logout),
]
