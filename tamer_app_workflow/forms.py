from django import forms

from tamer_app_workflow.models import TamerWorkflow, TamerState, TamerObject, TamerAction, TamerStateEdge, TamerEdge, TamerActionEdge


class TamerWorkflowForm(forms.ModelForm):
    class Meta:
        model = TamerWorkflow
        fields = ['id', 'name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control border'}),
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 8, 'class': 'form-control border'}),
        }


class TamerStateForm(forms.ModelForm):
    class Meta:
        model = TamerState
        fields = ['id', 'name', 'description', 'is_first', 'is_last']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control border'}),
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 8, 'class': 'form-control border'}),
            'is_first': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-left:0; margin-top:10px'}),
            'is_last': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-left:0; margin-top:10px'}),
        }


class TamerObjectForm(forms.ModelForm):
    class Meta:
        model = TamerObject
        fields = ['id', 'name', 'description', 'table', 'default_workflow']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control border'}),
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 8, 'class': 'form-control border'}),
            'table': forms.TextInput(attrs={'class': 'form-control border'}),
            'default_workflow': forms.Select(attrs={'class': 'form-control border'}),
        }


class TamerActionForm(forms.ModelForm):
    class Meta:
        model = TamerAction
        fields = ['id', 'name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control border'}),
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 8, 'class': 'form-control border'}),
            # 'function': forms.Select(attrs={'class': 'form-control border'}),
        }


class TamerStateEdgeForm(forms.ModelForm):
    class Meta:
        model = TamerStateEdge
        fields = ['id', 'edge', 'state']
        widgets = {
            'state': forms.HiddenInput(),
            'edge': forms.Select(attrs={'class': 'form-control border'}),
        }


class TamerEdgeForm(forms.ModelForm):
    class Meta:
        model = TamerEdge
        fields = ['id', 'name', 'description','next_state']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control border'}),
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 8, 'class': 'form-control border'}),
            'next_state': forms.Select(attrs={'class': 'form-control border'}),
        }


class TamerActionEdgeForm(forms.ModelForm):
    class Meta:
        model = TamerActionEdge
        fields = ['id', 'action', 'edge']
        widgets = {
            'edge': forms.HiddenInput(),
            'action': forms.Select(attrs={'class': 'form-control border'}),
        }
