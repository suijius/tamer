import datetime

from django.db import models
from django.urls import reverse

from tamer_app_base.models import TamerObject


class TamerWorkflow(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        managed = False
        db_table = 'tamer_workflow'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tamer-workflow-view')

    def get_started_state(self):
        return TamerState.objects.get(workflow=self, is_first=True)


class TamerState(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_first = models.BooleanField(verbose_name='Первое состояние')
    is_last = models.BooleanField(verbose_name='Конечное состояние')
    workflow = models.ForeignKey(TamerWorkflow, on_delete=models.DO_NOTHING, verbose_name='Рабочий поток')
    active = models.BooleanField(verbose_name="Статус")

    class Meta:
        managed = False
        db_table = 'tamer_state'

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('tamer-state-detail')


class TamerAction(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(blank=True, verbose_name='Описание')
    function = models.CharField(max_length=255, blank=True, verbose_name='Обработчик')

    class Meta:
        managed = False
        db_table = 'tamer_action'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tamer-workflow-view')


class TamerEdge(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name='Что сделать')
    description = models.TextField(blank=True, verbose_name='Описание')
    next_state = models.ForeignKey(TamerState, on_delete=models.DO_NOTHING, verbose_name='Перевести в состояние', blank=True, null=True)
    workflow = models.ForeignKey(TamerWorkflow, on_delete=models.DO_NOTHING, verbose_name='Рабочий поток')
    active = models.BooleanField(verbose_name="Статус")

    class Meta:
        managed = False
        db_table = 'tamer_edge'

    def __str__(self):
        return self.name


class TamerActionEdge(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    action = models.ForeignKey(TamerAction, on_delete=models.DO_NOTHING, verbose_name='Действие')
    edge = models.ForeignKey(TamerEdge, on_delete=models.DO_NOTHING, verbose_name='Переход')
    params = models.TextField(blank=True, verbose_name='Параметры')
    attachment = models.FileField(upload_to='static/attachment', blank=True)

    class Meta:
        managed = False
        db_table = 'tamer_action_edge'

    def __str__(self):
        return '%s - %s' % (self.edge.name, self.action.name)


class TamerStateEdge(models.Model):
    id = models.AutoField(primary_key=True)
    state = models.ForeignKey(TamerState, on_delete=models.DO_NOTHING)
    edge = models.ForeignKey(TamerEdge, on_delete=models.DO_NOTHING, verbose_name="Возможные переходы")

    class Meta:
        managed = False
        db_table = 'tamer_state_edge'

    def __str__(self):
        return '%s - %s' % (self.state.name, self.edge.name)


class TamerInstance(models.Model):
    id = models.AutoField(primary_key=True)
    state = models.ForeignKey(TamerState, on_delete=models.DO_NOTHING)
    object_id = models.IntegerField()
    object_type = models.ForeignKey(TamerObject, on_delete=models.DO_NOTHING)
    description = models.TextField(blank=True)
    datetime = models.DateTimeField()
    user = models.IntegerField(blank=True)
    attachment = models.FileField(upload_to='tamer_app_base/static/attachment', blank=True)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, blank=True, null=True)
    is_delay = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'tamer_instance'

    def __str__(self):
        return '%s - %s' % (self.id, self.state)

    def workflow(self):
        return TamerState.objects.get(state=self.state).workflow

    @staticmethod
    def add_instance(attachment, last_instance, description, next_state=None):
        if len(attachment):
            instance = TamerInstance(attachment=attachment)
        else:
            instance = TamerInstance()

        instance.state = last_instance.state
        if next_state is not None:
            instance.state = next_state

        instance.is_delay = last_instance.is_delay
        instance.object_type = last_instance.object_type
        instance.datetime = datetime.datetime.today()
        instance.description = description
        instance.object_id = last_instance.object_id
        instance.parent_id = last_instance.parent_id
        instance.save()
        return instance
