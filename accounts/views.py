from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .forms import UserSignUpForm


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return redirect('/measures/')
        else:
            messages.error(request, 'Usuário e/ou senha inválidos.')

    else:
        if request.user.is_authenticated():
            return redirect('/measures/')

    context = {
        'form': UserSignUpForm(),
    }

    return render(request, "accounts/login.html", context)

def logout(request):
    auth.logout(request)
    return redirect(login)

def signup(request):
    response_data = {}
    response_data['result'] = 'error'
    response_data['message'] = 'Some error message'
    return JsonResponse(response_data)

def lookup(request, field, value):
    filter_dict = {}
    filter_dict[field] = value

    try:
        num_results = User.objects.filter(**filter_dict).count()
        response = {
            'query': {
                'field' : field,
                'value' : value,
            },
            'totalResults': num_results,
        }
    except Exception as e:
        response = {
            'error'         : e.__class__.__name__,
            'error-message' : str(e)
        }

    return JsonResponse(response)
