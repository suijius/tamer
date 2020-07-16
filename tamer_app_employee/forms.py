from django import forms
from tamer_app_employee.models import TamerEmployee, TamerPosition#, TamerKindContact


# Contact
class TamerEmployeeForm(forms.ModelForm):
    class Meta:
        model = TamerEmployee
        fields = ['id', 'name', 'position', 'begin', 'end']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control border'}),
            'position': forms.Select(attrs={'class': 'form-control border'}),
            'begin': forms.HiddenInput(),
            'end': forms.HiddenInput(),
        }


# Kind of Contact
class TamerPositionForm(forms.ModelForm):
    class Meta:
        model = TamerPosition
        fields = ['id', 'position', 'rate', 'begin', 'end']
        widgets = {
            'position': forms.TextInput(attrs={'class': 'form-control border'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control border'}),
            'begin': forms.DateInput(
                attrs={'class': 'form-control', 'data-provide': 'datepicker', 'data-date-language': 'ru', 'data-date-format': 'dd.mm.yyyy'}),
            'end': forms.DateInput(
                attrs={'class': 'form-control', 'data-provide': 'datepicker', 'data-date-language': 'ru', 'data-date-format': 'dd.mm.yyyy'}),
        }


# Contact Note
class TamerPosition1Form(forms.ModelForm):
    class Meta:
        model = TamerPosition
        fields = ['id', 'position', 'rate']
        widgets = {
        }
