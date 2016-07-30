from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^list$', views.measures_list),
    url(r'^delete/(\d+)', views.delete_measure),
    url(r'^edit/(\d+)', views.edit_measure),
    url(r'^export_pdf$', views.export_pdf),
]
