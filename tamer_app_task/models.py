from django.db import models

from tamer_app_base.models import TamerObject
from tamer_app_workflow.models import TamerStateEdge, TamerInstance


class TamerTask(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    subject = models.CharField(max_length=200, verbose_name='Название задачи')
    description = models.TextField(verbose_name='Подробное описание')
    start = models.DateField(verbose_name='Дата начала')
    planning = models.DateField(verbose_name='Планируемая дата завершения')
    estimate = models.FloatField(verbose_name='Оценка трудозатрат')
    is_archive = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'tamer_task'

    def __str__(self):
        return self.subject

    object_type = None

    @staticmethod
    def set_object_type():
        if TamerTask.object_type is None:
            TamerTask.object_type = TamerObject.object_type(TamerTask)

    def get_instance_list(self):
        instances = TamerInstance.objects.filter(object_id=self.id,
                                                 object_type=self.object_type).order_by('-datetime')

        return instances

    def is_delay(self):
        message = ''
        if self.get_instance_list()[0].is_delay:
            message = '(Ожидание дочерних задач)'
        return message

    def get_current_status(self):
        instance_list = self.get_instance_list()
        if len(instance_list):
            return instance_list[0].state

        return None

    def get_possible_actions_annotation(self):
        edges = TamerStateEdge.objects.filter(state=self.get_current_status())
        return '\n '.join([item.edge.name for item in edges])

    def get_possible_actions(self):
        edges = TamerStateEdge.objects.filter(state=self.get_current_status())
        return edges

    workflow = None

    def get_workflow(self):
        if self.workflow is None:
            self.workflow = self.get_current_status().workflow
        return self.workflow


TamerTask.set_object_type()
# # Integration with workflow
# try:
#     from tamer_app_workflow.models import TamerInstance
# except Exception as e:
#     class TamerInstanceManager(models.Manager):
#         def all(self):
#             return []
#
#         def get_queryset(self):
#             return []
#
#
#     class TamerInstance(models.Model):
#         objects = TamerInstanceManager()
#
# try:
#     from tamer_app_workflow.models import TamerStateEdge
# except Exception as e:
#     class TamerTamerStateEdgeManager(models.Manager):
#         def all(self):
#             return []
#
#         def get_queryset(self):
#             return []
#
#
#     class TamerTamerStateEdge(models.Model):
#         objects = TamerTamerStateEdgeManager()
#
# #
# #
# # class TamerTaskWorkflow(models.Model):
# #     id = models.AutoField(primary_key=True, verbose_name="ID")
# #     task = models.ForeignKey(TamerTask, on_delete=models.DO_NOTHING, verbose_name="Задача")
# #     instance = models.ForeignKey(TamerInstance, on_delete=models.DO_NOTHING, verbose_name="Бизнес процесс")
# #     description = models.TextField(verbose_name="Дополнительное описание")
# #
# #     class Meta:
# #         managed = False
# #         db_table = 'tamer_task_instance'
#
# # def __str__(self):
# #     return self.contact.__str__()
