import json
import os
import subprocess
import datetime

import django_tables2 as tables
from django.forms import ModelChoiceField, Select, DateField, FileField
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DetailView, DeleteView

from tamer import settings
from tamer_app_base.commons import TamerCommon
from tamer_app_workflow.commons import TamerAppWorkflowCommon, TamerStateCommon, TamerActionCommon, TamerEdgeCommon
from tamer_app_workflow.forms import TamerWorkflowForm, TamerStateForm, TamerObjectForm, TamerActionForm, \
    TamerStateEdgeForm, TamerEdgeForm, \
    TamerActionEdgeForm
from tamer_app_workflow.models import TamerWorkflow, TamerObject, TamerAction, TamerState, TamerEdge, TamerStateEdge, \
    TamerActionEdge
from tamer_app_workflow.tables import TamerWorkflowTable, TamerObjectTable, TamerActionTable, TamerStateTable, \
    TamerEdgeTable, \
    TamerInactiveEdgeTable, TamerInactiveStateTable, TamerStateEdgeTable, TamerActionEdgeTable

from tamer_app_workflow import action


def req_state(state, list_uml, state_id=0):
    uml_text = ''
    mark = '<<Success>>'
    list_se = TamerStateEdge.objects.filter(state=state)
    for se in list_se:
        next_state = se.edge.next_state
        if next_state is None:
            next_state = state
        req_text = ''
        if next_state.active and state.active:
            actions_in_edge = TamerActionEdge.objects.filter(edge=se.edge)
            action_txt = ''
            for action in actions_in_edge:
                try:
                    params = json.loads(action.params)
                    # action.id = action.id#params.get('workflow', 0)
                    # if action.id != 0:
                    req_text = 'state_%s --> ' % state.id
                    state_txt = 'state_%s' % action.id
                    req_text += state_txt + ':%s\n' % se.edge.name
                    # код рабочий, не удалять
                    # req_text += 'state ' + state_txt + '{\n' + create_plantuml_text(int(action.id)).
                    # replace('@startuml', '').replace('@enduml', '') + '\n}\n'
                    req_text += state_txt + ' --> '
                    req_text += 'state_%s\n' % next_state.id
                    if next_state.id != state_id:
                        mark = ''
                    req_text += '\nstate "' + params['subject'] + '" as state_%s %s\n' % (action.id, mark)
                    # req_text += 'state_%s:%s\n' % (action.id, params.get('description', params['description']))
                    try:
                        list_uml.index(req_text)
                    except Exception:
                        list_uml.append(req_text)
                        action_txt += req_text
                except Exception as e:
                    pass
            if action_txt == '':
                req_text = 'state_%s --> state_%s:%s\n' % (state.id, next_state.id, se.edge.name)
            else:
                uml_text += action_txt
                req_text = 'state_%s --> state_%s:%s\n' % (state.id, next_state.id, se.edge.name)
                list_uml.append(req_text)
                req_text = ''

        try:
            list_uml.index(req_text)
        except Exception:
            list_uml.append(req_text)
            uml_text += req_text
            uml_text += req_state(next_state, list_uml)

    return uml_text


def create_plantuml_text(workflow, state_id=0, is_delay=False):
    states = TamerState.objects.filter(workflow=workflow, is_first=True, active=True)
    if len(states):
        initial_state = states[0]
        if is_delay:
            warning_color = 'Yellow'
        else:
            warning_color = 'LightGreen'
        uml_text = '''
@startuml
    skinparam state {
        EndColor Red
        BackgroundColor White
        BackgroundColor<<Success>> LightGreen
        BackgroundColor<<Warning>> %s
    }
    [*] --> state_%s
    ''' % (warning_color, initial_state.id)

        req_text = req_state(initial_state, [uml_text], state_id)
        uml_text += req_text

        for state in TamerState.objects.filter(workflow_id=workflow.id, active=True):
            if state_id == state.id:
                uml_text += 'state "%s" as state_%s <<Warning>>\n' % (state.name, state.id)
            else:
                uml_text += 'state "%s" as state_%s\n' % (state.name, state.id)

            uml_text += 'state_%s:%s\n' % (state.id, state.description)

        close_states = TamerState.objects.filter(workflow_id=workflow.id, is_last=True, active=True)
        for state in close_states:
            uml_text += 'state_%s --> [*]\n' % state.id

        uml_text += 'hide empty description\n scale 630 width\n @enduml'
        return uml_text

    return ''


def create_plantuml(workflow, state_id=0, file_name='', is_delay=False):
    uml_text = create_plantuml_text(workflow, state_id, is_delay)

    if file_name != '':
        path = os.path.join(settings.STATICFILES_DIRS[1], file_name)
    else:
        path = os.path.join(settings.STATICFILES_DIRS[1], 'workflow\\%s.txt' % workflow.id)

    f = open(path, 'w')
    f.writelines(uml_text)
    f.close()

    cmd = 'java -jar c:\\Users\\chepurnov_s\\devel\\tamer\\plantuml.jar %s' % path
    p = subprocess.Popen(cmd, shell=False)
    p.wait()
    p.kill()


class TamerWorkflowView(TamerAppWorkflowCommon, tables.SingleTableView):
    template_name = 'workflow_main.html'
    model = TamerWorkflow
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_table'] = TamerObjectTable(TamerObject.objects.all())
        context['workflow_table'] = TamerWorkflowTable(TamerWorkflow.objects.all())
        context['action_table'] = TamerActionTable(TamerAction.objects.all())
        return context


class TamerWorkflowCreate(TamerAppWorkflowCommon, CreateView):
    template_name = 'create-update.html'
    model = TamerWorkflow
    form_class = TamerWorkflowForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой записи рабочего потока'
        return context


class TamerWorkflowDetail(TamerAppWorkflowCommon, DetailView):
    template_name = 'workflow-detail.html'
    model = TamerWorkflow

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Просмотр записи рабочего потока'
        context['state_table'] = TamerStateTable(TamerState.objects.filter(workflow=self.object, active=True))
        context['edge_table'] = TamerEdgeTable(TamerEdge.objects.filter(workflow=self.object, active=True))
        context['inactive_state_table'] = TamerInactiveStateTable(
            TamerState.objects.filter(workflow=self.object, active=False))
        context['inactive_edge_table'] = TamerInactiveEdgeTable(
            TamerEdge.objects.filter(workflow=self.object, active=False))
        return context

    def get(self, request, *args, **kwargs):
        ret = super().get(request, *args, **kwargs)
        create_plantuml(self.object)
        return ret


class TamerWorkflowUpdate(TamerAppWorkflowCommon, UpdateView):
    template_name = 'create-update.html'
    model = TamerWorkflow
    form_class = TamerWorkflowForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Редактирование записи рабочего потока'
        return context


class TamerWorkflowDelete(TamerAppWorkflowCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerWorkflow
    success_url = reverse_lazy('tamer-workflow-view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи рабочего потока'
        return context


class TamerStateView(TamerAppWorkflowCommon, tables.SingleTableView):
    template_name = 'workflow_main.html'
    model = TamerState
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_table'] = TamerActionTable(TamerAction.objects.all())
        return context


class TamerStateCreate(TamerAppWorkflowCommon, CreateView):
    template_name = 'create-update.html'
    model = TamerState
    form_class = TamerStateForm
    # success_url = reverse_lazy('tamer-workflow-detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой записи состояния рабочего потока'
        return context

    def post(self, request, *args, **kwargs):
        workflow = self.request.GET.get('workflow', 0)
        self.success_url = '/workflow/%s' % (workflow)
        p = super().post(request, *args, **kwargs)
        self.object.workflow_id = workflow
        self.object.active = 1
        self.object.save()
        return p


class TamerStateDetail(TamerStateCommon, DetailView):
    template_name = 'state-update.html'
    model = TamerState

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Просмотр записи состояния рабочего потока'
        context['state_edge_table'] = TamerStateEdgeTable(TamerStateEdge.objects.filter(state=self.object))
        return context


class TamerStateUpdate(TamerStateCommon, UpdateView):
    template_name = 'create-update.html'
    model = TamerState
    form_class = TamerStateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Редактирование записи состояния рабочего потока'
        return context


class TamerStateDelete(TamerAppWorkflowCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerState

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи состояния рабочего потока'
        if not self.object.active:
            context['label'] = 'Восстановление записи состояния рабочего потока'
            context['delete_title'] = 'Вы точно хотите восстановить запись - '
            context['delete_button_caption'] = 'Восстановить'
            workflow = self.request.GET.get('workflow', 0)
            context['cancel_url'] = '/workflow/%s' % (workflow)
        return context

    def post(self, request, *args, **kwargs):
        workflow = self.request.GET.get('workflow', 0)
        self.success_url = '/workflow/%s' % (workflow)
        object = TamerState.objects.get(id=kwargs['pk'])
        object.active = not object.active
        object.save()

        return HttpResponseRedirect(self.success_url)


class TamerObjectCreate(TamerAppWorkflowCommon, CreateView):
    template_name = 'create-update.html'
    model = TamerObject
    form_class = TamerObjectForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой объекта автоматизации'
        return context


class TamerObjectUpdate(TamerAppWorkflowCommon, UpdateView):
    template_name = 'create-update.html'
    model = TamerObject
    form_class = TamerObjectForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Редактирование записи объекта автоматизации'
        return context


class TamerObjectDelete(TamerAppWorkflowCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerObject
    success_url = reverse_lazy('tamer-workflow-view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи объекта автоматизации'
        return context


class TamerActionCreate(TamerActionCommon, CreateView):
    template_name = 'create-update.html'
    model = TamerAction
    form_class = TamerActionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой записи действия рабочего потока'
        return context


class TamerActionUpdate(TamerActionCommon, UpdateView):
    template_name = 'create-update.html'
    model = TamerAction
    form_class = TamerActionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Редактирование записи действия рабочего потока'
        context['form'].fields['function'].initial = context[
            'object'].function  # context['form'].fields['function'].choices[context['object'].function]
        return context


class TamerActionDelete(TamerAppWorkflowCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerAction
    success_url = reverse_lazy('tamer-workflow-view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи действия рабочего потока'
        return context


class TamerStateEdgeCreate(TamerAppWorkflowCommon, CreateView):
    template_name = 'create-update.html'
    model = TamerStateEdge
    form_class = TamerStateEdgeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой записи перехода рабочего потока'
        path = self.request.GET.get('state', 0)
        context['parent_get_link'] = '/?state=%s' % path
        context['parent_link'] = '/state/%s' % path
        if path != 0:
            item_id = path.strip('/').split('/')[-1]
            context['form'].fields['state'].initial = TamerState.objects.get(id=item_id)
            context['form'].fields['edge'].choices = [[item.id, item.name] for item in
                                                      TamerEdge.objects.filter(
                                                          workflow=TamerState.objects.get(id=item_id).workflow,
                                                          active=True)]
        return context

    def post(self, request, *args, **kwargs):
        path = self.request.GET.get('state', 0)
        if path != 0:
            item_id = path.strip('/').split('/')[-1]
            TamerState.objects.get(id=item_id)
            self.success_url = '/state/%s?workflow=%s' % (item_id, TamerState.objects.get(id=item_id).workflow.id)
        return super().post(request, *args, **kwargs)


class TamerStateEdgeDelete(TamerAppWorkflowCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerStateEdge

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи действия рабочего потока'
        return context

    def post(self, request, *args, **kwargs):
        path = self.request.GET.get('state', 0)
        if path != 0:
            item_id = path.strip('/').split('/')[-1]
            TamerState.objects.get(id=item_id)
            self.success_url = '/state/%s?workflow=%s' % (item_id, TamerState.objects.get(id=item_id).workflow.id)
        return super().post(request, *args, **kwargs)


class TamerEdgeView(TamerAppWorkflowCommon, tables.SingleTableView):
    template_name = 'workflow_main.html'
    model = TamerEdge
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_table'] = TamerActionTable(TamerAction.objects.all())
        return context


class TamerEdgeCreate(TamerEdgeCommon, CreateView):
    template_name = 'create-update.html'
    model = TamerEdge
    form_class = TamerEdgeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой записи состояния рабочего потока'
        context['parent_link'] = '/workflow/%s' % self.request.GET.get('workflow', 0)
        return context

    def post(self, request, *args, **kwargs):
        workflow = self.request.GET.get('workflow', 0)
        self.success_url = '/workflow/%s' % (workflow)
        p = super().post(request, *args, **kwargs)
        self.object.workflow_id = workflow
        self.object.active = 1
        self.object.save()
        return p


class TamerEdgeDetail(TamerAppWorkflowCommon, DetailView):
    template_name = 'edge-update.html'
    model = TamerEdge

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Просмотр записи состояния рабочего потока'
        context['action_edge_table'] = TamerActionEdgeTable(TamerActionEdge.objects.filter(edge=self.object))
        context['parent_link'] = '/workflow/%s' % self.object.workflow.id
        return context


class TamerEdgeUpdate(TamerEdgeCommon, UpdateView):
    template_name = 'create-update.html'
    model = TamerEdge
    form_class = TamerEdgeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Редактирование записи состояния рабочего потока'
        context['form'].fields['next_state'].initial = context['object'].next_state
        return context

    def post(self, request, *args, **kwargs):
        edge = kwargs.get('pk', 0)
        self.success_url = '/edge/%s' % edge
        return super().post(request, *args, **kwargs)


class TamerEdgeDelete(TamerAppWorkflowCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerEdge
    success_url = reverse_lazy('tamer-workflow-view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи действия рабочего потока'
        if not self.object.active:
            context['label'] = 'Восстановление записи действия рабочего потока'
            context['delete_title'] = 'Вы точно хотите восстановить запись - '
            context['delete_button_caption'] = 'Восстановить'
            workflow = self.request.GET.get('workflow', 0)
            context['cancel_url'] = '/workflow/%s' % (workflow)

        return context

    def post(self, request, *args, **kwargs):
        workflow = self.request.GET.get('workflow', 0)
        self.success_url = '/workflow/%s' % (workflow)
        object = TamerEdge.objects.get(id=kwargs['pk'])
        object.active = not object.active
        object.save()

        return HttpResponseRedirect(self.success_url)


class TamerActionEdgeCreate(TamerAppWorkflowCommon, CreateView):
    template_name = 'create-update.html'
    model = TamerActionEdge
    form_class = TamerActionEdgeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой записи действия рабочего потока'
        path = self.request.GET.get('edge', 0)
        context['parent_get_link'] = '/?edge=%s' % path
        context['parent_link'] = '/edge/%s' % path
        if path != 0:
            item_id = path.strip('/').split('/')[-1]
            context['form'].fields['edge'].initial = TamerEdge.objects.get(id=item_id)
            context['form'].fields['action'].choices = [[item.id, item.name] for item in
                                                        TamerAction.objects.all()]
        return context

    def post(self, request, *args, **kwargs):
        path = self.request.GET.get('edge', 0)
        if path != 0:
            item_id = path.strip('/').split('/')[-1]
            TamerEdge.objects.get(id=item_id)
            self.success_url = '/edge/%s?workflow=%s' % (item_id, TamerEdge.objects.get(id=item_id).workflow.id)
        return super().post(request, *args, **kwargs)


class TamerActionEdgeUpdate(TamerAppWorkflowCommon, UpdateView):
    template_name = 'create-update.html'
    model = TamerActionEdge
    form_class = TamerActionEdgeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fun_object = action.get_action(self.object.action.function)
        action_form = fun_object.getformset(self.object)

        params = {}
        try:
            params = json.loads(self.object.params)
        except:
            pass
        for param, value in params.items():
            if type(action_form.fields[param]) is DateField:
                d_value = datetime.datetime.today()
                try:
                    d_value = datetime.datetime.strptime(value, "%d.%m.%Y %H:%M")
                except:
                    pass
                try:
                    d_value = datetime.datetime.strptime(value, "%d.%m.%Y").date()
                except:
                    pass
                action_form.fields[param].initial = d_value
            elif type(action_form.fields[param]) is ModelChoiceField:
                pk_name = action_form.fields[param].queryset.model._meta.pk.name
                if value != '':
                    action_form.fields[param].initial = action_form.fields[param].queryset.filter(**{pk_name: value})[0]
            elif type(action_form.fields[param]) is FileField:
                label = action_form.fields[param].label
                action_form.fields[param].label = label + ' ' + self.object.attachment.name.split('/')[-1]
            else:
                action_form.fields[param].initial = params[param]

        context['form'] = action_form
        context['label'] = 'Редактирование записи действия рабочего потока'
        path = self.request.GET.get('edge', 0)
        context['parent_get_link'] = '/?edge=%s' % path
        context['parent_link'] = '/edge/%s' % path
        return context

    def post(self, request, *args, **kwargs):
        path = self.request.GET.get('edge', 0)
        if path != 0:
            item_id = path.strip('/').split('/')[-1]
            TamerEdge.objects.get(id=item_id)
            self.success_url = '/edge/%s?workflow=%s' % (item_id, TamerEdge.objects.get(id=item_id).workflow.id)

        params = {}
        object = TamerActionEdge.objects.get(id=kwargs['pk'])
        fun_object = action.get_action(object.action.function)
        action_form = fun_object.getformset(object)
        for param, value in request.POST.items():
            if param in action_form.fields.keys():
                params[param] = value
        if len(request.FILES.get('attachment', [])):
            object.attachment = request.FILES['attachment']
            object.save()
            params['attachment'] = object.attachment.path
        object.params = json.dumps(params)
        object.save()

        return HttpResponseRedirect(self.success_url)


class TamerActionEdgeDelete(TamerAppWorkflowCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerActionEdge
    # success_url = reverse_lazy('tamer-workflow-view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи действия рабочего потока'
        path = self.request.GET.get('edge', 0)
        self.success_url = '/edge/%s' % path
        return context


