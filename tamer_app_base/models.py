from django.db import models


class TamerObject(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(blank=True, verbose_name='Описание')
    table = models.CharField(max_length=255, verbose_name='Таблица из БД')
    default_workflow = models.IntegerField(db_column='default_workflow_id', verbose_name='Рабочий поток по умолчанию')

    class Meta:
        managed = False
        db_table = 'tamer_objects'

    def __str__(self):
        return self.name

    @staticmethod
    def object_type(model):
        items = TamerObject.objects.filter(table=model._meta.db_table)
        task_object_type = 0
        if len(items) > 0:
            task_object_type = items[0]
        return task_object_type



