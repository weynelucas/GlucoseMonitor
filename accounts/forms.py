from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from django.contrib.auth import update_session_auth_hash
from parsley.decorators import parsleyfy
from django.core.mail import mail_admins, send_mail
from django.template.loader import render_to_string

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
class PasswordUpdateForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Senha atual'}), required=True)
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Nova senha'}), required=True)
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Confirmar nova senha'}), required=True)

    def __init__(self, request):
        self.request = request
        super(self.__class__, self).__init__(user=request.user or None, data=request.POST or None)

    def save(self):
        super(self.__class__, self).save()
        update_session_auth_hash(self.request, self.user)

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


TOPIC_CHOICES = (
    ('general', 'Geral'),
    ('bug-report', 'Relatar bug'),
    ('suggestion', 'Sugestão'),
)

@parsleyfy
class ContactForm(forms.Form):
    topic   = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), label='Tópico', choices=TOPIC_CHOICES, initial='general', required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Mensagem'}), label='Mensagem', max_length=750, required=True)

    def send(self, sender):
        context = {
            'topic'  : dict(self.fields['topic'].choices)[self.cleaned_data['topic']],
            'message': self.cleaned_data['message'],
            'sender' : sender,
        }

        message_plain = render_to_string('accounts/mail/contact.txt', context)
        message_html  = render_to_string('accounts/mail/contact.html', context)

        send_mail(
            "GlucoseMonitor - %s" % (context['topic'].upper()),
            message_plain,
            "weynelucas@gmail.com",
            ["weynelucas@gmail.com"],
            html_message = message_html,
            fail_silently=False,
        )
