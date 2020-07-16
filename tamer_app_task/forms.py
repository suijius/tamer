from ckeditor.widgets import CKEditorWidget
from django import forms

from tamer_app_task.models import TamerTask


class TamerTaskForm(forms.ModelForm):
    class Meta:
        model = TamerTask
        fields = ['id', 'subject', 'description', 'start', 'planning', 'estimate']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control border'}),
            'description': CKEditorWidget(config_name='basic', attrs={'class': 'form-control border'}),
            'start': forms.DateInput(
                attrs={'class': 'form-control', 'data-provide': 'datepicker', 'data-date-language': 'ru',
                       'data-date-format': 'dd.mm.yyyy'}),
            'planning': forms.DateInput(
                attrs={'class': 'form-control', 'data-provide': 'datepicker', 'data-date-language': 'ru',
                       'data-date-format': 'dd.mm.yyyy'}),
            'estimate': forms.NumberInput(attrs={'class': 'form-control border'}),
        }
