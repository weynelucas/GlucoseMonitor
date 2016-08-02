from django.shortcuts import render
from .forms import UserSignUpForm

# Create your views here.
def login(request):
    return render(request, "accounts/login.html", {'form': UserSignUpForm()})
