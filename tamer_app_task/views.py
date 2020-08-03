import datetime

from django.db import connections
from django.db.models import Subquery
from django.forms import ModelChoiceField, Select, CharField, Textarea, FileField, FileInput
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
import django_tables2 as tables

from tamer_app_base.models import TamerObject
from tamer_app_task.commons import TamerAppTaskCommon
from tamer_app_task.forms import TamerTaskForm
from tamer_app_task.models import TamerTask
from tamer_app_task.tables import TamerTaskTable

# Integration with workflow
from tamer_app_workflow.views import create_plantuml
from tamer_app_workflow import action
from tamer_app_workflow.models import TamerWorkflow, TamerInstance, TamerEdge, TamerState, TamerActionEdge

# Integration with Todoist
import todoist

from tamer import settings


class TamerTaskView(TamerAppTaskCommon, tables.SingleTableView):
    template_name = 'task_view.html'
    model = TamerTask
    table_class = TamerTaskTable
    paginate_by = 20

    def get_context_data(self, **kwargs):
        query_state = ['''SELECT distinct i.object_id
                        FROM (SELECT distinct i.object_id, state_id, i.object_type_id
from tamer_instance i) as i
                        join tamer_state as s on i.state_id = s.id
                        where object_type_id = 2
                        group by i.object_id
                        having count(*)=1 and max(s.is_first)''',
                       '''SELECT distinct i.object_id
                       FROM (SELECT distinct i.object_id, state_id, i.object_type_id
from tamer_instance i) as i
                       join tamer_state as s on i.state_id = s.id
                       where object_type_id = 2
                       group by i.object_id
                       having not max(s.is_last) and count(*)>1;''',
                       '''SELECT distinct i.object_id
                       FROM (SELECT distinct i.object_id, state_id, i.object_type_id
from tamer_instance i) as i
                       join tamer_state as s on i.state_id = s.id
                       where object_type_id = 2 and s.is_last''',
                       ]
        context = super().get_context_data(**kwargs)
        request_path = self.request.path.strip('/') + '?' + ', '.join(
            ['%s=%s' % (key, value) for key, value in self.request.GET.items()])
        request_path = request_path.strip('?')
        caption = ''
        for item in self.menu['menu']:
            submenu = item.get('submenu', [])
            for subitem in submenu:
                if request_path == subitem['link']:
                    caption = subitem['title']
                    break
            if len(submenu):
                continue
            if caption != '':
                break
            if request_path == item['link']:
                caption = item['title']
                break

        context['caption'] = caption
        workflow_id = self.request.GET.get('workflow', None)
        state = self.request.GET.get('state', None)
        is_archive = self.request.GET.get('is_archive', False)
        # task_list = []
        if workflow_id is not None:
            state_list = TamerState.objects.filter(workflow_id=workflow_id)
            instance_list = TamerInstance.objects.filter(state__in=Subquery(state_list.values('pk')),
                                                         object_type=TamerTask.object_type)
            task_list = TamerTask.objects.filter(is_archive=False,
                                                 id__in=Subquery(instance_list.values('object_id'))).order_by(
                '-planning')
            context['table'] = TamerTaskTable(task_list)
        elif state is not None:
            with connections['default'].cursor() as cursor:
                cursor.execute(query_state[int(state)])
                result = [item[0] for item in cursor.fetchall()]
                task_list = TamerTask.objects.filter(is_archive=False, id__in=result).order_by('-planning')
                context['table'] = TamerTaskTable(task_list)
        else:
            query_active = query_state[0] + ' union ' + query_state[1]
            with connections['default'].cursor() as cursor:
                cursor.execute(query_active)
                result = [item[0] for item in cursor.fetchall()]
                task_list = TamerTask.objects.filter(is_archive=is_archive, id__in=result).order_by('-planning')
                context['table'] = TamerTaskTable(task_list)

        context['gantt_data'] = [dict(Task=item.subject, Start=item.start, Finish=item.planning, Complete=50) for item
                                 in task_list]
        return context


class TamerTaskCreate(TamerAppTaskCommon, CreateView):
    template_name = 'create-update.html'
    model = TamerTask
    form_class = TamerTaskForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой задачи'
        context['form'].fields['workflow'] = ModelChoiceField(TamerWorkflow.objects)
        context['form'].fields['workflow'].widget = Select(attrs={'class': 'chzn-select chosen_select form-control'})
        context['form'].fields['workflow'].label = 'Рабочий поток'
        context['form'].fields['workflow'].choices = [[item.id, item.name] for item in
                                                      TamerWorkflow.objects.all()]
        return context

    def post(self, request, *args, **kwargs):
        p = super().post(request, *args, **kwargs)
        workflow_id = self.request.POST.get('workflow', 0)

        initial_state = TamerWorkflow.objects.get(id=workflow_id).get_started_state()
        instance = TamerInstance()
        instance.state = initial_state
        instance.object_type = TamerObject.object_type(self.model)
        instance.datetime = datetime.datetime.today()
        instance.desc = 'create'
        instance.object_id = self.object.id
        instance.save()

        pid = settings.TODOIST_TAMER_ID
        api = todoist.TodoistAPI(settings.TODOIST)
        item = api.items.add(self.object.subject, project_id=pid, due={"date": self.object.planning})
        note = api.notes.add(item.temp_id, self.object.description)
        api.commit()
        self.object.todoist_item_id = item.temp_id
        self.object.todoist_note_id = note.temp_id
        self.object.save()
        return p


class TamerTaskUpdate(TamerAppTaskCommon, UpdateView):
    template_name = 'update.html'
    model = TamerTask
    form_class = TamerTaskForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Редактирование записи задачи'
        context['form'].fields['edge'] = ModelChoiceField(TamerEdge.objects)
        context['form'].fields['edge'].widget = Select(attrs={'class': 'chzn-select chosen_select form-control'})
        context['form'].fields['edge'].label = 'Действие'
        context['form'].fields['edge'].choices = [[0, 'Оставить комментарий']] + [[item.edge.id, item.edge.name] for
                                                                                  item in
                                                                                  self.object.get_possible_actions()]
        context['form'].fields['edge_desc'] = CharField()
        context['form'].fields['edge_desc'].widget = Textarea(
            attrs={'cols': 80, 'rows': 8, 'class': 'span form-control'})
        context['form'].fields['edge_desc'].label = 'Комментарий к действию'

        context['form'].fields['attachment'] = FileField()
        context['form'].fields['attachment'].widget = FileInput(attrs={'class': 'form-control', 'style': 'border:none'})
        context['form'].fields['attachment'].label = 'Вложения'
        context['form'].fields['attachment'].required = False

        context['parent_link'] = reverse_lazy('tamer-task-view')

        activity = ''
        current_state = ''
        instance_list = self.object.get_instance_list()
        for instance in reversed(instance_list):
            path = ''
            if instance.attachment != '':
                path = 'link<' + 'attachment\\%s' % instance.attachment.name.split('/')[-1] + '>'

            if instance.description == 'create':
                activity += '<b><u>' + instance.state.name + ' ' + instance.datetime.strftime(
                    "%d.%m.%Y %H:%M") + '</u></b>\n'
                current_state = instance.state.name
            else:
                if current_state != instance.state.name:
                    activity += '<b><u>' + instance.state.name + ' ' + instance.datetime.strftime(
                        "%d.%m.%Y %H:%M") + '</u></b>\n'
                    current_state = instance.state.name
                if instance.description == '' and path != '':
                    instance.description = 'Приложение'
                activity += instance.datetime.strftime(
                    "%d.%m.%Y %H:%M") + ' ' + instance.description + ' ' + path + '\n'
        context['action'] = activity
        return context

    def post(self, request, *args, **kwargs):
        p = super().post(request, *args, **kwargs)
        attachment = request.FILES.get('attachment', [])
        last_instance = TamerTask.get_instance_list(self=self.object)[0]
        description = self.request.POST.get('edge_desc', '')
        next_state = None

        edge_id = self.request.POST.get('edge', 0)
        if edge_id != '0':
            edge = TamerEdge.objects.get(id=edge_id)
            next_state = edge.next_state
            ae = TamerActionEdge.objects.filter(edge=edge)
            for item in ae:
                fun_object = action.get_action(item.action.function)
                params = fun_object.execute(item, self.object.id)
                last_instance = TamerTask.get_instance_list(self=self.object)[0]
                # next_state = last_instance.state
                TamerInstance.add_instance(attachment, last_instance, '%s - %s' % (item.action.name, params['subject']), next_state)

        instance = TamerInstance.add_instance(attachment, last_instance, description, next_state)
        create_plantuml(self.object.get_workflow(), instance.state.id, 'workflow\\task\\%s.txt' % self.object.id,
                        instance.is_delay)

        pid = settings.TODOIST_TAMER_ID
        api = todoist.TodoistAPI(settings.TODOIST)
        if self.object.todoist_item_id is None:
            item = api.items.add(self.object.subject, project_id=pid, due={"date": self.object.planning})
            note = api.notes.add(item.temp_id, self.object.description)
            self.object.todoist_item_id = item.temp_id
            self.object.todoist_note_id = note.temp_id
            self.object.save()
        else:
            api.items.update(self.object.todoist_item_id, content=self.object.subject, due={"date": self.object.planning})
            api.notes.update(self.object.todoist_note_id, content=self.object.description)
            api.notes.add(self.object.todoist_item_id, description)
            if instance.state.is_last:
                api.items.complete(self.object.todoist_item_id)
        api.commit()

        return p


class TamerTaskDelete(TamerAppTaskCommon, DeleteView):
    model = TamerTask
    success_url = reverse_lazy('tamer-task-view')

    def post(self, request, *args, **kwargs):
        item = self.model.objects.get(id=kwargs['pk'])
        item.is_archive = True
        item.save()

        api = todoist.TodoistAPI(settings.TODOIST)
        api.items.delete(item.todoist_item_id)
        api.commit()

        return HttpResponseRedirect(self.success_url)
