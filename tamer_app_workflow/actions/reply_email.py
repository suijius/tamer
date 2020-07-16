import win32com.client
from subprocess import Popen
from django.forms import FileInput, FileField
from django.forms import modelformset_factory

# from dashboard.models import DashboardTask as db_task
#
# from root.views.workflow.action import ActionView
# from root.models import DashboardWFInstance as db_instance
from tamer_app_workflow.commons import ActionView


class ReplyEmail(ActionView):
    label = 'Выбор шаблона письма'

    # @staticmethod
    # def getparams():
    #     return {}
    #
    # @staticmethod
    # def getformset_factory():
    #     formset_factory = modelformset_factory(
    #         db_task,
    #         exclude=(),
    #         fields=(),
    #         widgets={
    #         })
    #     return formset_factory
    #
    # @staticmethod
    # def getformset(edge):
    #     action_formset = ReplyEmail.getformset_factory()
    #     formset = action_formset(queryset=db_task.objects.none())
    #
    #     formset.forms[0].fields['attachment'] = FileField()
    #     formset.forms[0].fields['attachment'].widget = FileInput(attrs={'class': 'form-control', 'style': 'border:none'})
    #     formset.forms[0].fields['attachment'].label = 'Шаблон письма - '
    #
    #     return formset
    #
    # @staticmethod
    # def execute(ae, object_id):
    #     instance = db_instance.objects.filter(object_id=object_id).order_by('datetime')
    #     cmd = '"C:\\Program Files (x86)\\Microsoft Office\\Office16\\outlook" /f %s' % instance[0].attachment.path
    #     Popen(cmd)
