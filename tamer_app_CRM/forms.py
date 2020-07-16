from django import forms

from tamer_app_CRM.models import TamerCustomer, TamerOpportunity, TamerContract, TamerOpportunityContact


class TamerCustomerForm(forms.ModelForm):
    class Meta:
        model = TamerCustomer
        fields = ['id', 'name', 'description']
        widgets = {
            'name': forms.Textarea(attrs={'cols': 80, 'rows': 8, 'class': 'form-control border'}),
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 8, 'class': 'form-control border'}),
        }


class TamerOpportunityForm(forms.ModelForm):
    class Meta:
        model = TamerOpportunity
        fields = ['id', 'subject', 'customer', 'description']
        widgets = {
            'subject': forms.Textarea(attrs={'cols': 80, 'rows': 8, 'class': 'form-control border'}),
            'customer': forms.Select(attrs={'class': 'form-control border'}),
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 8, 'class': 'form-control border'}),
        }


class TamerContractForm(forms.ModelForm):
    class Meta:
        model = TamerContract
        fields = ['id', 'amount', 'margin', 'contract', 'customer', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control border'}),
            'margin': forms.NumberInput(attrs={'class': 'form-control border'}),
            'contract': forms.Textarea(attrs={'cols': 80, 'rows': 8, 'class': 'form-control border'}),
            'customer': forms.Select(attrs={'class': 'form-control border'}),
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 8, 'class': 'form-control border'}),
        }


class TamerOpportunityContactForm(forms.ModelForm):
    class Meta:
        model = TamerOpportunityContact
        fields = ['id', 'contact', 'opportunity', 'description']
        widgets = {
            'opportunity': forms.HiddenInput(),
            'contact': forms.Select(attrs={'class': 'form-control border'}),
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 8, 'class': 'form-control border'})
        }
