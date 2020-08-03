from django.db import models
from django.urls import reverse

# from tamer_app_base.models import TamerDocumentSection, TamerDocument


class TamerProject(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    subject = models.CharField(max_length=200, blank=True, null=True, verbose_name='Наименование проекта')
    contract_amount = models.FloatField(blank=True, null=True, verbose_name='Сумма контракта')
    start = models.DateField(verbose_name='Начало')
    finish = models.DateField(verbose_name='Окончание')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:
        managed = False
        db_table = 'tamer_project'

    def __str__(self):
        return '%s (%s)' % (self.subject, self.id)

    @staticmethod
    def get_absolute_url():
        return reverse('tamer-project-view')


class TamerStage(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    project = models.ForeignKey(TamerProject, models.DO_NOTHING)
    number = models.IntegerField(blank=False, null=False, verbose_name="Номер этапа")
    amount = models.FloatField(blank=True, null=True, verbose_name="Сумма этапа")
    start = models.DateField(verbose_name="Начало этапа")
    finish = models.DateField(verbose_name="Окончание этапа")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        managed = False
        db_table = 'tamer_stage'

    def __str__(self):
        return 'Этап %s %s' % (self.number, self.project.subject)


class TamerSubcontract(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    project = models.ForeignKey(TamerProject, models.DO_NOTHING)
    subject = models.TextField(blank=False, null=False, verbose_name="Субподрядчик")
    amount = models.FloatField(blank=True, null=True, verbose_name="Сумма")
    start = models.DateField(verbose_name="Начало")
    finish = models.DateField(verbose_name="Окончание")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        managed = False
        db_table = 'tamer_subcontract'

    def __str__(self):
        return '%s %s' % (self.subject, self.project.subject)


class TamerEquipment(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    project = models.ForeignKey(TamerProject, models.DO_NOTHING)
    subject = models.TextField(blank=False, null=False, verbose_name="Оборудование")
    amount = models.FloatField(blank=True, null=True, verbose_name="Сумма")
    start = models.DateField(verbose_name="Начало")
    finish = models.DateField(verbose_name="Окончание")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        managed = False
        db_table = 'tamer_equipment'

    def __str__(self):
        return '%s %s' % (self.subject, self.project.subject)


class TamerEducation(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    project = models.ForeignKey(TamerProject, models.DO_NOTHING)
    subject = models.TextField(blank=False, null=False, verbose_name="Обучение")
    amount = models.FloatField(blank=True, null=True, verbose_name="Сумма")
    start = models.DateField(verbose_name="Начало")
    finish = models.DateField(verbose_name="Окончание")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        managed = False
        db_table = 'tamer_education'

    def __str__(self):
        return '%s %s' % (self.subject, self.project.subject)


class TamerBusinessTrip(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    project = models.ForeignKey(TamerProject, models.DO_NOTHING)
    subject = models.TextField(blank=False, null=False, verbose_name="Командировки")
    amount = models.FloatField(blank=True, null=True, verbose_name="Сумма")
    start = models.DateField(verbose_name="Начало")
    finish = models.DateField(verbose_name="Окончание")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        managed = False
        db_table = 'tamer_business_trip'

    def __str__(self):
        return '%s %s' % (self.subject, self.project.subject)
