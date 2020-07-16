import inspect
import os
import sys
from imp import load_source

from django.db.models import QuerySet
from django.forms import ModelChoiceField, Select
from django.views import View
from tamer_app_base.commons import TamerCommon
from tamer_app_workflow.models import TamerState
import tamer_app_workflow.actions as actions


class ActionView(View):
    label = 'Наименование обработчика по умолчанию'

    @staticmethod
    def getparams():
        return {}

    @staticmethod
    def getform(edge):
        return {}


class TamerAppWorkflowCommon(TamerCommon):
    menu = {'menu': [{'title': 'Рабочие потоки', 'link': 'workflow', 'sidebar_link': 'workflow'},
                     {'title': 'Состояния потоков', 'link': 'instance', 'sidebar_link': 'workflow'},
                     ]}
    title = 'Рабочие потоки'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.sidebar_link = 'workflow'
        return context


class TamerPostCommon(TamerAppWorkflowCommon):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_get_link'] = '/?project=%s' % self.request.GET.get('project', 0)
        context['parent_link'] = '/project/%s' % self.request.GET.get('project', 0)
        return context

    def post(self, request, *args, **kwargs):
        self.success_url = '/project/%s' % request.GET.get('project', 0)
        return super().post(request, *args, **kwargs)


class TamerStateCommon(TamerAppWorkflowCommon):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_get_link'] = '/?workflow=%s' % self.request.GET.get('workflow', 0)
        context['parent_link'] = '/workflow/%s' % self.request.GET.get('workflow', 0)
        return context

    def post(self, request, *args, **kwargs):
        self.success_url = '/state/%s?workflow=%s' % (kwargs['pk'], self.request.GET.get('workflow', 0))
        return super().post(request, *args, **kwargs)


class TamerActionCommon(TamerAppWorkflowCommon):
    @staticmethod
    def get_functions():
        path_list = os.listdir(globals()['actions'].__path__[0])
        functions = []
        for l in path_list:
            modulename = inspect.getmodulename(l)
            try:
                load_source(modulename, globals()['actions'].__path__[0] + '//' + l)

                classes = []
                for cls_name, cls_obj in inspect.getmembers(sys.modules[modulename]):
                    if inspect.isclass(cls_obj) and issubclass(cls_obj, ActionView) and cls_name != 'ActionView':
                        classes.append([cls_name, cls_obj])
                functions += classes
            except AttributeError:
                pass
        return functions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        functions = self.get_functions()
        context['form'].fields['function'] = ModelChoiceField(QuerySet())
        context['form'].fields['function'].label = 'Обработчик'
        context['form'].fields['function'].widget = Select(attrs={'class': 'form-control border'})
        context['form'].fields['function'].choices = [[cls_name, cls_obj.label] for cls_name, cls_obj in functions]
        return context


class TamerEdgeCommon(TamerAppWorkflowCommon):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = context.get('object', 0)
        if object == 0:
            workflow_id = self.request.GET.get('workflow', 0)
        else:
            workflow_id = object.workflow_id
        context['form'].fields['next_state'] = ModelChoiceField(QuerySet())
        context['form'].fields['next_state'].label = 'Перевести в состояние'
        context['form'].fields['next_state'].widget = Select(attrs={'class': 'form-control border'})
        context['form'].fields['next_state'].choices = [[item.id, item.name] for item in
                                                        TamerState.objects.filter(workflow_id=workflow_id)]
        return context


