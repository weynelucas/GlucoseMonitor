from django.contrib.auth.models import User
from django import forms
from parsley.decorators import parsleyfy
from parsley.decorators import parsleyfy


@parsleyfy
class UserSignUpForm(forms.ModelForm):
    password_confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Confirmar senha'}), required=True)
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
            'password_confirmation': {
                'equalto': 'password',
                'equalto-message': 'A senha e a confirmação de senha devem ser iguais.'
            }
        }
