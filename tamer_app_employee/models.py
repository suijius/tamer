from django.db import models
from django.urls import reverse
import datetime


class TamerPositionManager(models.Manager):
    def get_queryset(self):
        today = datetime.date.today()
        return super().get_queryset().filter(end__gt=today).order_by('position')
        # return super().get_queryset().filter(begin__date__lte=time, end__date__gt=time).order_by('position')


class TamerPosition(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    position = models.CharField(max_length=200, verbose_name='Роль')
    rate = models.FloatField(verbose_name='Рейт')
    begin = models.DateField(verbose_name='Начало действия')
    end = models.DateField(verbose_name='Окончание действия')
    objects = TamerPositionManager()

    class Meta:
        managed = False
        db_table = 'tamer_position'

    def __str__(self):
        return '%s: %02d.%02d.%s-%02s.%02s.%s' % (self.position, self.begin.day, self.begin.month, self.begin.year, self.end.day, self.end.month, self.end.year)

    def get_absolute_url(self):
        return reverse('tamer-position-view')


class TamerEmployeeManager(models.Manager):
    def get_queryset(self):
        time = datetime.datetime.now()
        return super().get_queryset().filter(begin__date__lte=time, end__date__gt=time).order_by('name')


class TamerEmployee(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=200, verbose_name='Имя')
    position = models.ForeignKey(TamerPosition, verbose_name='Проектная роль', on_delete=models.DO_NOTHING)
    begin = models.DateTimeField(verbose_name='Начало действия')
    end = models.DateTimeField(verbose_name='Окончание действия')
    objects = TamerEmployeeManager()

    class Meta:
        managed = False
        db_table = 'tamer_employee'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tamer-employee-view')


# class TamerEmployeePosition(models.Model):
#     id = models.AutoField(primary_key=True, verbose_name='ID')
#     position = models.ForeignKey(TamerPosition, verbose_name='', on_delete=models.DO_NOTHING)
#     employee = models.ForeignKey(TamerEmployee, verbose_name='', on_delete=models.DO_NOTHING)
#     rate = models.IntegerField()
#     begin = models.DateTimeField()
#     end = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'tamer_employee_position'
#
#     def __str__(self):
#         return '%s-%s' % (self.employee.name, self.position.position)
#
#     def get_absolute_url(self):
#         return reverse('tamer-employee-position-view')
