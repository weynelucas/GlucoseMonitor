from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import UserSignUpForm, PasswordChangeForm


def login(request):
    if request.method == 'POST':
        next_path = request.POST.get('next', '/measures/')
        username  = request.POST['username']
        password  = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return redirect(next_path)
        else:
            messages.error(request, 'Usuário e/ou senha inválidos.')

    else:
        next_path = request.GET.get('next', '/measures/')
        if request.user.is_authenticated():
            return redirect(next_path)

    context = {
        'form': UserSignUpForm(),
        'next': next_path
    }

    return render(request, "accounts/login.html", context)

def logout(request):
    auth.logout(request)
    return redirect(login)

def signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = auth.authenticate(username=request.POST['username'], password=request.POST['password1'])
            if new_user is not None and new_user.is_active:
                auth.login(request, new_user)
                return redirect('/measures/')

    return redirect(login)

@login_required
def set_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Senha alterada com sucesso.')
            return redirect('/measures/')
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form': form
    }
    return render(request, 'accounts/modal/set_password.html', context)




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

@login_required
def check_password(request, password):
    response = {}
    response['check'] = request.user.check_password(password)
    return JsonResponse(response)
