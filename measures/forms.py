from django import forms
from measures.models import GlucoseMeasure
from parsley.decorators import parsleyfy

attrs = {
    'class': 'form-control',
}

@parsleyfy
class GlucoseMeasureForm(forms.ModelForm):
    class Meta:
        model = GlucoseMeasure
        fields = ['value', 'datetime', 'notes', 'user']
        widgets = {
            'value'   : forms.NumberInput(attrs=attrs),
            'datetime': forms.DateTimeInput(attrs=attrs),
            'notes'   : forms.Textarea(attrs=attrs),
            'user'    : forms.HiddenInput()
        }
        labels = {
            'value'   : 'Valor',
            'datetime': 'Dia e horário',
            'notes'   : 'Notas',
            'user'    : 'Usuário',
        }
        parsley_extras = {
            'value'   : {
                'pattern'         : '^\d{1,3}([\.\,]\d{0,2})?$',
                'pattern-message' : 'Por favor insira um número válido.',
                'type-message'    : 'Por favor insira um número válido.',
                'required-message': 'Este campo é obrigatório.',
            }
        }
