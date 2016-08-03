from django.shortcuts import render, redirect
from django.template import RequestContext

def page_not_found(request):
    return render(request, 'error/404.html', RequestContext(request))

def server_error(request):
    return render(request, 'error/500.html', RequestContext(request))

def permission_denied(request):
    return render(request, 'error/403.html', RequestContext(request))

def bad_request(request):
    return render(request, 'error/400.html', RequestContext(request))
