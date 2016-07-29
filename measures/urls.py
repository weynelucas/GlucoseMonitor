from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^list$', views.measures_list),
    url(r'^export_pdf$', views.export_pdf),
]
