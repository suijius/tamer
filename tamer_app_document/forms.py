from django import forms
from ckeditor.widgets import CKEditorWidget

from tamer_app_document.models import TamerDocumentTemplate, TamerDocumentTemplateSection, TamerDocument, \
    TamerDocumentSection


class TamerDocumentTemplateForm(forms.ModelForm):
    class Meta:
        model = TamerDocumentTemplate
        fields = ['id', 'type', 'description']
        widgets = {
            'type': forms.TextInput(attrs={'class': 'form-control border'}),
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 8, 'class': 'form-control border'}),
        }


class TamerDocumentTemplateSectionForm(forms.ModelForm):
    class Meta:
        model = TamerDocumentTemplateSection
        fields = ['id', 'section', 'sort', 'description', 'document_template']
        widgets = {
            'document_template': forms.HiddenInput(),
            'section': forms.TextInput(attrs={'class': 'form-control border'}),
            'sort': forms.NumberInput(attrs={'class': 'form-control border'}),
            'description': CKEditorWidget(config_name='default', attrs={'cols': 80, 'rows': 8, 'class': 'form-control border'}),
        }


class TamerDocumentForm(forms.ModelForm):
    class Meta:
        model = TamerDocument
        fields = ['id', 'name', 'document_template']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control border'}),
            'document_template': forms.Select(attrs={'class': 'form-control border'}),
        }


class TamerDocumentSectionCreateForm(forms.ModelForm):
    class Meta:
        model = TamerDocumentSection
        fields = ['id', 'sort', 'section', 'document']
        widgets = {
            'document': forms.HiddenInput(),
            'section': forms.TextInput(attrs={'class': 'form-control border'}),
            'sort': forms.NumberInput(attrs={'class': 'form-control border'}),
        }


class TamerDocumentSectionUpdateForm(forms.ModelForm):
    class Meta:
        model = TamerDocumentSection
        fields = ['id', 'sort', 'section', 'document', 'description']
        widgets = {
            'document': forms.HiddenInput(),
            'section': forms.TextInput(attrs={'class': 'form-control border'}),
            'sort': forms.NumberInput(attrs={'class': 'form-control border'}),
            'description': CKEditorWidget(attrs={'cols': 80, 'rows': 8, 'class': 'form-control border'}),
        }

# class TamerProjectCharterForm(forms.ModelForm):
#     class Meta:
#         model = TamerProjectCharter
#         fields = ['id', 'project', 'subject', 'amount', 'start', 'finish', 'description']
#         widgets = {
#             'project': forms.HiddenInput(),
#             'subject': forms.TextInput(attrs={'class': 'form-control border'}),
#             'amount': forms.NumberInput(attrs={'class': 'form-control border'}),
#             'start': forms.DateInput(
#                 attrs={'class': 'form-control', 'data-provide': 'datepicker', 'data-date-language': 'ru',
#                        'data-date-format': 'dd.mm.yyyy'}),
#             'finish': forms.DateInput(
#                 attrs={'class': 'form-control', 'data-provide': 'datepicker', 'data-date-language': 'ru',
#                        'data-date-format': 'dd.mm.yyyy'}),
#             'description': forms.Textarea(attrs={'cols': 80, 'rows': 8, 'class': 'form-control border'}),
#         }