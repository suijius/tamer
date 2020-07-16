from django.utils.safestring import mark_safe
from django_tables2.utils import A
import django_tables2 as tables

from tamer_app_base.tables import TamerTableCommon
from tamer_app_document.models import TamerDocumentTemplate, TamerDocumentTemplateSection, TamerDocument, \
    TamerDocumentSection


class TamerDocumentTemplateTable(TamerTableCommon, tables.Table):
    id = tables.TemplateColumn(
        '<a href="{% url "tamer-document-template-detail" record.id %}">'
        '{{ record.id }}</a>')
    type = tables.TemplateColumn(
        '<a href="{% url "tamer-document-template-detail" record.id %}">'
        '{{ record.type }}</a>')
    remove = tables.TemplateColumn(
        '<a class="far fa-trash-alt" href="{% url "tamer-document-template-delete" record.id %}">'
        '</a>', verbose_name=mark_safe('<i class="fas fa-cogs"></i>'), orderable=False)

    class Meta(TamerTableCommon.Meta):
        model = TamerDocumentTemplate
        exclude = ()
        prefix = 'document-template-'


class TamerDocumentTemplateSectionTable(TamerTableCommon, tables.Table):
    id = tables.TemplateColumn(
        '<a href="{% url "tamer-document-template-section-update" record.id %}?document_template={{ view.object.id }}">'
        '{{ record.id }}</a>')
    section = tables.TemplateColumn(
        '<a href="{% url "tamer-document-template-section-update" record.id %}?document_template={{ view.object.id }}">'
        '{{ record.section }}</a>')
    remove = tables.TemplateColumn(
        '<a class="far fa-trash-alt" href="{% url "tamer-document-template-section-delete" record.id %}?document_template='
        '{{ view.object.id }}">'
        '</a>', verbose_name=mark_safe('<i class="fas fa-cogs"></i>'), orderable=False)

    class Meta(TamerTableCommon.Meta):
        model = TamerDocumentTemplateSection
        exclude = ('document_template', 'id')
        prefix = 'document-template-section-'


class TamerDocumentTable(TamerTableCommon, tables.Table):
    id = tables.TemplateColumn(
        '<a href="{% url "tamer-document-detail" record.id %}">'
        '{{ record.id }}</a>')
    name = tables.TemplateColumn(
        '<a href="{% url "tamer-document-detail" record.id %}">'
        '{{ record.name }}</a>')
    remove = tables.TemplateColumn(
        '<a class="far fa-trash-alt" href="{% url "tamer-document-delete" record.id %}">'
        '</a>', verbose_name=mark_safe('<i class="fas fa-cogs"></i>'), orderable=False)

    class Meta(TamerTableCommon.Meta):
        model = TamerDocument
        exclude = ()
        prefix = 'document-'


class TamerDocumentSectionTable(TamerTableCommon, tables.Table):
    id = tables.TemplateColumn(
        '<a href="{% url "tamer-document-section-update" record.id %}?document={{ view.object.id }}">'
        '{{ record.id }}</a>')
    section = tables.TemplateColumn(
        '<a href="{% url "tamer-document-section-update" record.id %}?document={{ view.object.id }}">'
        '{{ record.section }}</a>')
    remove = tables.TemplateColumn(
        '<a class="far fa-trash-alt" href="{% url "tamer-document-section-delete" record.id %}?document='
        '{{ view.object.id }}">'
        '</a>', verbose_name=mark_safe('<i class="fas fa-cogs"></i>'), orderable=False)
    document_template = tables.Column(visible=False)

    class Meta(TamerTableCommon.Meta):
        model = TamerDocumentSection
        exclude = ()
        prefix = 'document-section-'
