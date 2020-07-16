from django import forms

from tamer_app_project.models import TamerProject, TamerStage, TamerSubcontract, TamerBusinessTrip, TamerEquipment, \
    TamerEducation


class TamerProjectForm(forms.ModelForm):
    class Meta:
        model = TamerProject
        fields = ['id', 'subject', 'contract_amount', 'start', 'finish', 'description']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control border'}),
            'contract_amount': forms.NumberInput(attrs={'class': 'form-control border'}),
            'start': forms.DateInput(
                attrs={'class': 'form-control', 'data-provide': 'datepicker', 'data-date-language': 'ru',
                       'data-date-format': 'dd.mm.yyyy'}),
            'finish': forms.DateInput(
                attrs={'class': 'form-control', 'data-provide': 'datepicker', 'data-date-language': 'ru',
                       'data-date-format': 'dd.mm.yyyy'}),
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 8, 'class': 'form-control border'}),
        }


class TamerStageForm(forms.ModelForm):
    class Meta:
        model = TamerStage
        fields = ['id', 'project', 'number', 'amount', 'start', 'finish', 'description']
        widgets = {
            'project': forms.HiddenInput(),
            'number': forms.TextInput(attrs={'class': 'form-control border'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control border'}),
            'start': forms.DateInput(
                attrs={'class': 'form-control', 'data-provide': 'datepicker', 'data-date-language': 'ru',
                       'data-date-format': 'dd.mm.yyyy'}),
            'finish': forms.DateInput(
                attrs={'class': 'form-control', 'data-provide': 'datepicker', 'data-date-language': 'ru',
                       'data-date-format': 'dd.mm.yyyy'}),
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 8, 'class': 'form-control border'}),
        }


class TamerSubcontractForm(forms.ModelForm):
    class Meta:
        model = TamerSubcontract
        fields = ['id', 'project', 'subject', 'amount', 'start', 'finish', 'description']
        widgets = {
            'project': forms.HiddenInput(),
            'subject': forms.TextInput(attrs={'class': 'form-control border'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control border'}),
            'start': forms.DateInput(
                attrs={'class': 'form-control', 'data-provide': 'datepicker', 'data-date-language': 'ru',
                       'data-date-format': 'dd.mm.yyyy'}),
            'finish': forms.DateInput(
                attrs={'class': 'form-control', 'data-provide': 'datepicker', 'data-date-language': 'ru',
                       'data-date-format': 'dd.mm.yyyy'}),
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 8, 'class': 'form-control border'}),
        }


class TamerEducationForm(forms.ModelForm):
    class Meta:
        model = TamerEducation
        fields = ['id', 'project', 'subject', 'amount', 'start', 'finish', 'description']
        widgets = {
            'project': forms.HiddenInput(),
            'subject': forms.TextInput(attrs={'class': 'form-control border'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control border'}),
            'start': forms.DateInput(
                attrs={'class': 'form-control', 'data-provide': 'datepicker', 'data-date-language': 'ru',
                       'data-date-format': 'dd.mm.yyyy'}),
            'finish': forms.DateInput(
                attrs={'class': 'form-control', 'data-provide': 'datepicker', 'data-date-language': 'ru',
                       'data-date-format': 'dd.mm.yyyy'}),
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 8, 'class': 'form-control border'}),
        }


class TamerEquipmentForm(forms.ModelForm):
    class Meta:
        model = TamerEquipment
        fields = ['id', 'project', 'subject', 'amount', 'start', 'finish', 'description']
        widgets = {
            'project': forms.HiddenInput(),
            'subject': forms.TextInput(attrs={'class': 'form-control border'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control border'}),
            'start': forms.DateInput(
                attrs={'class': 'form-control', 'data-provide': 'datepicker', 'data-date-language': 'ru',
                       'data-date-format': 'dd.mm.yyyy'}),
            'finish': forms.DateInput(
                attrs={'class': 'form-control', 'data-provide': 'datepicker', 'data-date-language': 'ru',
                       'data-date-format': 'dd.mm.yyyy'}),
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 8, 'class': 'form-control border'}),
        }


class TamerBusinessTripForm(forms.ModelForm):
    class Meta:
        model = TamerBusinessTrip
        fields = ['id', 'project', 'subject', 'amount', 'start', 'finish', 'description']
        widgets = {
            'project': forms.HiddenInput(),
            'subject': forms.TextInput(attrs={'class': 'form-control border'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control border'}),
            'start': forms.DateInput(
                attrs={'class': 'form-control', 'data-provide': 'datepicker', 'data-date-language': 'ru',
                       'data-date-format': 'dd.mm.yyyy'}),
            'finish': forms.DateInput(
                attrs={'class': 'form-control', 'data-provide': 'datepicker', 'data-date-language': 'ru',
                       'data-date-format': 'dd.mm.yyyy'}),
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 8, 'class': 'form-control border'}),
        }



