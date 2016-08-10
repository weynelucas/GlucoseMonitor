"""GlucoseMonitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, handler400, handler403, handler404, handler500
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import bad_request, permission_denied, page_not_found, server_error

urlpatterns = [
    url(r'^', include('favicon.urls')),
    url(r'^', include('accounts.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^measures/', include('measures.urls')),
]

handler400 = 'GlucoseMonitor.views.bad_request'
handler403 = 'GlucoseMonitor.views.permission_denied'
handler404 = 'GlucoseMonitor.views.page_not_found'
handler500 = 'GlucoseMonitor.views.server_error'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
