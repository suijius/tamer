from django.db import models
from django.urls import reverse

from tamer_app_base.models import TamerObject


class TamerDocumentTemplate(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    type = models.CharField(max_length=200, verbose_name='Тип документа')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        managed = False
        db_table = 'tamer_document_template'

    def __str__(self):
        return self.type

    def get_absolute_url(self):
        return reverse('tamer-document-template-view')


class TamerDocumentTemplateSection(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    sort = models.IntegerField(verbose_name="Номер раздела")
    section = models.CharField(max_length=200, verbose_name='Раздел документа')
    description = models.TextField(verbose_name='Рекомендации по заполнению')
    document_template = models.ForeignKey(TamerDocumentTemplate, on_delete=models.DO_NOTHING, verbose_name='Тип документа')

    class Meta:
        managed = False
        db_table = 'tamer_document_template_section'

    def __str__(self):
        return '%s (%s)' % (self.name, self.id)


class TamerDocument(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=250, verbose_name="Наименование документа")
    document_template = models.ForeignKey(TamerDocumentTemplate, on_delete=models.DO_NOTHING, verbose_name="Шаблон документа")

    class Meta:
        managed = False
        db_table = 'tamer_document'

    def __str__(self):
        return '%s (%s)' % (self.name, self.id)

    def get_absolute_url(self):
        return reverse('tamer-document-view')


class TamerDocumentSection(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    document = models.ForeignKey(TamerDocument, on_delete=models.DO_NOTHING, verbose_name="Документ")
    sort = models.IntegerField(verbose_name="Номер раздела")
    section = models.CharField(max_length=250, verbose_name="Раздел документа")
    description = models.TextField(verbose_name="Содержание")
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'tamer_document_section'

    def __str__(self):
        return self.section

