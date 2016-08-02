from django.contrib.auth.models import User
from django import forms
from parsley.decorators import parsleyfy
from parsley.decorators import parsleyfy


@parsleyfy
class UserSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nome'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Sobrenome'}),
            'username'  : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nome de usuário'}),
            'email'     : forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Endereço de email'}),
            'password'  : forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Senha'}),
        }
