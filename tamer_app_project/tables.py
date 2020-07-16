from django.utils.safestring import mark_safe
from django_tables2.utils import A
import django_tables2 as tables

from tamer_app_base.tables import TamerTableCommon
from tamer_app_project.models import TamerProject, TamerStage, TamerSubcontract, TamerEquipment, TamerEducation, \
    TamerBusinessTrip


class TamerProjectTable(TamerTableCommon, tables.Table):
    id = tables.LinkColumn('tamer-project-detail', args=[A('pk')])
    subject = tables.LinkColumn('tamer-project-detail', args=[A('pk')])
    remove = tables.LinkColumn('tamer-project-delete', args=[A('pk')],
                               verbose_name=mark_safe('<i class="fas fa-cogs"></i>'),
                               text=mark_safe('<i class="far fa-trash-alt"></i>'), orderable=False)

    class Meta(TamerTableCommon.Meta):
        model = TamerProject


class TamerStageTable(TamerTableCommon, tables.Table):
    id = tables.TemplateColumn(
        '<a href="{% url "tamer-stage-detail" record.id %}?project={{ view.object.id }}">{{ record.id }}</a>')
    number = tables.TemplateColumn(
        '<a href="{% url "tamer-stage-detail" record.id %}?project={{ view.object.id }}">{{ record.number }}</a>')
    remove = tables.TemplateColumn(
        '<a class="far fa-trash-alt" href="{% url "tamer-stage-delete" record.id %}?project={{ view.object.id }}">'
        '</a>', verbose_name=mark_safe('<i class="fas fa-cogs"></i>'), orderable=False)

    class Meta(TamerTableCommon.Meta):
        model = TamerStage
        exclude = ('project',)
        prefix = 'stage-'


class TamerSubcontractTable(TamerTableCommon, tables.Table):
    id = tables.TemplateColumn(
        '<a href="{% url "tamer-subcontract-detail" record.id %}?project={{ view.object.id }}">'
        '{{ record.id }}</a>')
    subject = tables.TemplateColumn(
        '<a href="{% url "tamer-subcontract-detail" record.id %}?project={{ view.object.id }}">'
        '{{ record.subject }}</a>')
    remove = tables.TemplateColumn(
        '<a class="far fa-trash-alt" href="{% url "tamer-subcontract-delete" record.id %}?project='
        '{{ view.object.id }}">'
        '</a>', verbose_name=mark_safe('<i class="fas fa-cogs"></i>'), orderable=False)

    class Meta(TamerTableCommon.Meta):
        model = TamerSubcontract
        prefix = 'subcontract-'


class TamerEquipmentTable(TamerTableCommon, tables.Table):
    id = tables.TemplateColumn(
        '<a href="{% url "tamer-equipment-detail" record.id %}?project={{ view.object.id }}">{{ record.id }}</a>')
    subject = tables.TemplateColumn(
        '<a href="{% url "tamer-equipment-detail" record.id %}?project={{ view.object.id }}">{{ record.subject }}</a>')
    remove = tables.TemplateColumn(
        '<a class="far fa-trash-alt" href="{% url "tamer-equipment-delete" record.id %}?project={{ view.object.id }}">'
        '</a>', verbose_name=mark_safe('<i class="fas fa-cogs"></i>'), orderable=False)

    class Meta(TamerTableCommon.Meta):
        model = TamerEquipment
        exclude = ('project',)
        prefix = 'equipment-'


class TamerEducationTable(TamerTableCommon, tables.Table):
    id = tables.TemplateColumn(
        '<a href="{% url "tamer-education-detail" record.id %}?project={{ view.object.id }}">{{ record.id }}</a>')
    subject = tables.TemplateColumn(
        '<a href="{% url "tamer-education-detail" record.id %}?project={{ view.object.id }}">{{ record.subject }}</a>')
    remove = tables.TemplateColumn(
        '<a class="far fa-trash-alt" href="{% url "tamer-education-delete" record.id %}?project={{ view.object.id }}">'
        '</a>', verbose_name=mark_safe('<i class="fas fa-cogs"></i>'), orderable=False)

    class Meta(TamerTableCommon.Meta):
        model = TamerEducation
        exclude = ('project',)
        prefix = 'education-'


class TamerBusinessTripTable(TamerTableCommon, tables.Table):
    id = tables.TemplateColumn(
        '<a href="{% url "tamer-business-trip-detail" record.id %}?project={{ view.object.id }}">'
        '{{ record.id }}</a>')
    subject = tables.TemplateColumn(
        '<a href="{% url "tamer-business-trip-detail" record.id %}?project={{ view.object.id }}">'
        '{{ record.subject }}</a>')
    remove = tables.TemplateColumn(
        '<a class="far fa-trash-alt" href="{% url "tamer-business-trip-delete" record.id %}?project='
        '{{ view.object.id }}">'
        '</a>', verbose_name=mark_safe('<i class="fas fa-cogs"></i>'), orderable=False)

    class Meta(TamerTableCommon.Meta):
        model = TamerBusinessTrip
        exclude = ('project',)
        prefix = 'business-trip-'
