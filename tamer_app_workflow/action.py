import inspect
import os
import sys
from imp import load_source

from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.forms import NumberInput, TextInput, DateInput, HiddenInput, CheckboxInput, Select
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.forms.models import ModelChoiceField

from tamer_app_workflow.models import TamerAction as db_action
import tamer_app_workflow.actions as actions

@login_required
def create_action(request):
    action_formset = modelformset_factory(
        db_action,
        exclude=('id',),
        fields=('name', 'desc', 'function'),
        widgets={
            'name': TextInput(attrs={'class': 'form-control'}),
            'desc': TextInput(attrs={'class': 'form-control'}),
            'function': TextInput(attrs={'class': 'form-control'}),
        },
        error_messages={
            'id': {'unique': 'Проект с этим номером возможности уже существует'},
            'null': '',
            'blank': '',
            'invalid': '',
            'invalid_choice': '',
            'unique': '',
            'unique_for_date': ''}
    )

    if request.method == 'POST':
        formset = action_formset(request.POST)
        if formset.is_valid() and request.POST['form-0-id'] != 0:
            formset.save()
            return HttpResponseRedirect('/root/workflow')
    else:
        formset = action_formset(queryset=db_action.objects.none())

    return render(request, 'form/create-update.html',
                  {'formset': formset, 'label': 'Новое действие'})


@login_required
def update_action(request, action_id):
    action_formset = modelformset_factory(
        db_action,
        exclude=('id',),
        fields=('name', 'desc', 'function'),
        widgets={
            'name': TextInput(attrs={'class': 'form-control'}),
            'desc': TextInput(attrs={'class': 'form-control'}),
        },
        error_messages={
            'id': {'unique': 'Проект с этим номером возможности уже существует'},
            'null': '',
            'blank': '',
            'invalid': '',
            'invalid_choice': '',
            'unique': '',
            'unique_for_date': ''}
    )
    if request.method == 'POST':
        formset = action_formset(request.POST)
        if formset.is_valid() and request.POST['form-0-id'] != 0:
            formset.save()
            return HttpResponseRedirect('/root/workflow')
    else:
        formset = action_formset(queryset=db_action.objects.filter(id=action_id))

        path_list = os.listdir(globals()['actions'].__path__[0])
        functions = []
        for l in path_list:
            modulename = inspect.getmodulename(l)
            try:
                load_source(modulename, globals()['actions'].__path__[0] + '//' + l)
            # classes = [[cls_name, cls_obj] for cls_name, cls_obj in inspect.getmembers(sys.modules[modulename]) if inspect.isclass(cls_obj) and cls_name != 'ActionView']

                classes = []
                for cls_name, cls_obj in inspect.getmembers(sys.modules[modulename]):
                    if inspect.isclass(cls_obj) and issubclass(cls_obj, ActionView) and cls_name != 'ActionView':
                        classes.append([cls_name, cls_obj])
                functions += classes
            except AttributeError:
                pass

        formset.forms[0].fields['function'] = ModelChoiceField(QuerySet())
        formset.forms[0].fields['function'].widget = Select(attrs={'class': 'chzn-select chosen_select form-control'})
        formset.forms[0].fields['function'].label = 'Обработчик'
        formset.forms[0].fields['function'].choices = [[cls_name, cls_obj.label] for cls_name, cls_obj in functions]

    return render(request, 'form/create-update.html',
                  {'formset': formset, 'label': 'Изменение действия'})


class ActionView(View):
    label = 'Наименование обработчика по умолчанию'

    @staticmethod
    def getparams():
        return {}

    @staticmethod
    def getformset(edge):
        return {}


def get_action(fun_name):
    fun_object = None

    path_list = os.listdir(globals()['actions'].__path__[0])
    for l in path_list:
        modulename = inspect.getmodulename(l)
        load_source(modulename, globals()['actions'].__path__[0] + '//' + l)
        for cls_name, cls_obj in inspect.getmembers(sys.modules[modulename]):
            if fun_name == cls_name:
                fun_object = cls_obj
                break
        if fun_object:
            break

    return fun_object