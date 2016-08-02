from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
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
