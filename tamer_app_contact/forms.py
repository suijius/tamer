from django import forms
from tamer_app_contact.models import TamerContact, TamerKindContact, TamerContactNote


# Contact
class TamerContactForm(forms.ModelForm):
    class Meta:
        model = TamerContact
        fields = ['id', 'name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control border'}),
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 8, 'class': 'form-control border'}),
        }


# Kind of Contact
class TamerKindContactForm(forms.ModelForm):
    class Meta:
        model = TamerKindContact
        fields = ['id', 'name', 'sort']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control border'}),
            'sort': forms.NumberInput(attrs={'class': 'form-control border'})
        }


# Contact Note
class TamerContactNoteForm(forms.ModelForm):
    class Meta:
        model = TamerContactNote
        fields = ['id', 'contact', 'kind_contact', 'note']
        widgets = {
            'contact': forms.HiddenInput(),
            'kind_contact': forms.Select(attrs={'class': 'form-control border'}),
            'note': forms.Textarea(attrs={'class': 'form-control border'}),
        }
