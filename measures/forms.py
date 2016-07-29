from django import forms
from measures.models import GlucoseMeasure
from parsley.decorators import parsleyfy

attrs = {
    'value'       : {'class': 'form-control'} ,
    'datetime'    : {'class': 'form-control'} ,
    'measure_type': {'class': 'form-control'} ,
    'notes'       : {'class': 'form-control', 'rows': 6} ,
}

@parsleyfy
class GlucoseMeasureForm(forms.ModelForm):
    class Meta:
        model = GlucoseMeasure
        fields = ['measure_type', 'value', 'datetime', 'notes', 'user']
        widgets = {
            'value'       : forms.NumberInput(attrs=attrs['value']),
            'datetime'    : forms.DateTimeInput(attrs=attrs['datetime']),
            'notes'       : forms.Textarea(attrs=attrs['notes']),
            'measure_type': forms.Select(attrs=attrs['measure_type']),
            'user'        : forms.HiddenInput()
        }
        labels = {
            'value'       : 'Valor',
            'datetime'    : 'Data/Hora',
            'notes'       : 'Notas',
            'measure_type': 'Tipo',
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
                'pattern-message' : 'Por favor insira uma data/hora válida.',
            }
        }
