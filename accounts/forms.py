from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from parsley.decorators import parsleyfy


@parsleyfy
class UserSignUpForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Senha'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Confirmar senha'}), required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nome'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Sobrenome'}),
            'username'  : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nome de usuário'}),
            'email'     : forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Endereço de email'}),
        }
        parsley_extras = {
            'first_name': {
                'required': 'true',
                'required-message': 'Este campo é obrigatório.',
            },
            'last_name': {
                'required': 'true',
                'required-message': 'Este campo é obrigatório.',
            },
            'username': {
                'unique-username': 'true',
                'unique-username-message': 'Este nome de usuário já está em uso.',
            },
            'email': {
                'required': 'true',
                'unique-email': 'true',
                'unique-email-message': 'Este endereço de email já está em uso.',
                'required-message': 'Este campo é obrigatório.',
                'type-message': 'Por favor insira um endereço de email válido.',
            },
            'password2': {
                'equalto': 'password1',
                'equalto-message': 'A senha e a confirmação de senha devem ser iguais.'
            }
        }



@parsleyfy
class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Senha atual'}), required=True)
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Nova senha'}), required=True)
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Confirmar nova senha'}), required=True)
    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']
        parsley_extras = {
            'old_password': {
                'required': 'true',
                'password-check': 'true',
                'password-check-message': 'Sua senha está incorreta.',
                'required-message': 'Este campo é obrigatório.',
            },
            'new_password2': {
                'required': 'true',
                'required-message': 'Este campo é obrigatório.',
            },
            'new_password2': {
                'required': 'true',
                'equalto': 'new_password1',
                'equalto-message': 'A nova senha e a confirmação de nova senha devem ser iguais.',
                'required-message': 'Este campo é obrigatório.',
            }
        }
