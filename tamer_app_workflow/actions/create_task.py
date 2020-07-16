import datetime
import inspect
import json
import sys
from imp import load_source

from django.forms import Textarea, Select, DateInput, ModelChoiceField, DateField, FileField, forms
from django.forms import modelformset_factory

# from dashboard.models import DashboardTask as db_task
# from root.models import DashboardWorkflow as db_workflow
# from root.models import DashboardWFInstance as db_instance
# from root.models import DashboardObject as db_object
# from root.models import DashboardWFState as db_state
# from root.views.workflow import action
# from root.views.workflow.action import ActionView
from tamer_app_task.forms import TamerTaskForm
from tamer_app_task.models import TamerTask
from tamer_app_workflow.commons import ActionView
from tamer_app_workflow.models import TamerWorkflow, TamerInstance, TamerState
from tamer_app_workflow import action


class CreateTask(ActionView):
    label = 'Создание задачи'

    @staticmethod
    def getparams():
        return {}

    @staticmethod
    def getformset(ae):
        task_form = TamerTaskForm()
        task_form.fields['start'].initial = datetime.date.today()

        workflow = TamerWorkflow.objects.all()
        task_form.fields['workflow'] = ModelChoiceField(TamerWorkflow.objects)
        task_form.fields['workflow'].widget = Select(attrs={'class': 'chzn-select chosen_select form-control'})
        task_form.fields['workflow'].choices = [[item.id, item.name] for item in workflow]
        task_form.fields['workflow'].label = 'Рабочий поток'

        task_form.fields['subject'].initial = ae.action.name
        task_form.fields['description'].initial = ae.action.description

        return task_form

    @staticmethod
    def execute(ae, object_id):
        params = {}
        try:
            params = json.loads(ae.params)
        except:
            pass

        if len(params):
            parent_instance = TamerInstance.objects.filter(object_id=object_id).order_by('-datetime')
            parent_task = TamerTask.objects.get(id=object_id)
            task = TamerTask()

            fun_object = action.get_action(ae.action.function)
            action_form = fun_object.getformset(ae)
            for param, value in params.items():
                d_value = None
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
                elif type(action_form.fields[param]) is ModelChoiceField:
                    pk_name = action_form.fields[param].queryset.model._meta.pk.name
                    if value != '':
                        d_value = action_form.fields[param].queryset.filter(**{pk_name: value})[0]
                elif type(action_form.fields[param]) is FileField:
                    label = action_form.fields[param].label
                    d_value = label + ' ' + ae.attachment.name.split('/')[-1]
                else:
                    d_value = params[param]

                task.__dict__[param] = d_value
                if param == 'subject':
                    task.subject = parent_task.subject + "/" + d_value.replace('Создание задачи - ', '').capitalize()# + ' проекта: ' + task.opportunity.subject
                    task.subject.capitalize()



            task.save()

            states = TamerState.objects.filter(workflow=task.workflow, is_first=True)
            if len(states):
                initial_state = states[0]
                instance = TamerInstance()
                instance.state = initial_state
                instance.object_type = TamerTask.object_type
                instance.datetime = datetime.datetime.today()
                instance.description = 'create'
                instance.object_id = task.id
                if len(parent_instance):
                    instance.parent = parent_instance[0]
                instance.save()

            # if not parent_instance[0].is_delay:
            parent_instance[0].is_delay = True
            parent_instance[0].save()

        return params
