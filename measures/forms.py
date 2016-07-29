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
        fields = ['measure_type', 'value', 'datetime', 'notes', 'user']
        widgets = {
            'value'       : forms.NumberInput(attrs=attrs),
            'datetime'    : forms.DateTimeInput(attrs=attrs),
            'notes'       : forms.Textarea(attrs=attrs),
            'measure_type': forms.Select(attrs=attrs),
            'user'        : forms.HiddenInput()
        }
        labels = {
            'value'       : 'Valor',
            'datetime'    : 'Dia e horário',
            'notes'       : 'Notas',
            'measure_type': 'Tipe de medição',
            'user'        : 'Usuário',
        }
        parsley_extras = {
            'value'   : {
                'pattern'         : '^\d{1,3}([\.\,]\d{0,2})?$',
                'pattern-message' : 'Por favor insira um número válido.',
                'type-message'    : 'Por favor insira um número válido.',
                'required-message': 'Este campo é obrigatório.',
            },
            'datetime': {
                'pattern'         : '^([0-2][0-9]|[3][0-1])/([0][1-9]|[1][0-2])\/(\d{4})\ ([0-1][0-9]|[2][0-3])\:([0-5][0-9])(:([0-5][0-9]))?$',
                'pattern-message' : 'Por favor insira uma data no formato válido (dd/mm/aaaa hh:mm:ss).',
            }
        }
