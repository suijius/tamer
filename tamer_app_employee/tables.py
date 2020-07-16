from django.utils.safestring import mark_safe
from django_tables2 import A
import django_tables2 as tables

from tamer_app_base.tables import TamerTableCommon
from tamer_app_employee.models import TamerEmployee, TamerPosition#, TamerEmployeePosition


class TamerEmployeeTable(TamerTableCommon, tables.Table):
    id = tables.LinkColumn('tamer-employee-detail', args=[A('pk')])
    name = tables.LinkColumn('tamer-employee-detail', args=[A('pk')])
    remove = tables.LinkColumn('tamer-employee-delete', args=[A('pk')], verbose_name=mark_safe('<i class="fas fa-cogs"></i>'),
                               text=mark_safe('<i class="far fa-trash-alt"></i>'), orderable=False)
    end = tables.Column(visible=False)

    class Meta(TamerTableCommon.Meta):
        model = TamerEmployee


class TamerPositionTable(TamerTableCommon, tables.Table):
    id = tables.LinkColumn('tamer-position-detail', args=[A('pk')])
    position = tables.LinkColumn('tamer-position-detail', args=[A('pk')])
    rate = tables.LinkColumn('tamer-position-detail', args=[A('pk')])
    remove = tables.LinkColumn('tamer-position-delete', args=[A('pk')], verbose_name=mark_safe('<i class="fas fa-cogs"></i>'),
                               text=mark_safe('<i class="far fa-trash-alt"></i>'), orderable=False)
    # end = tables.Column(visible=False)

    class Meta(TamerTableCommon.Meta):
        model = TamerPosition


class TamerPosition1Table(TamerTableCommon, tables.Table):
    id = tables.TemplateColumn('<a href="{% url "tamer-position-detail" record.id %}?contact={{ view.object.id }}">{{ record.id }}</a>')
    position = tables.Column(visible=False)
    remove = tables.TemplateColumn('<a class="far fa-trash-alt" href="{% url "tamer-position-delete" record.id %}?contact={{ view.object.id }}">'
                                   '</a>', verbose_name=mark_safe('<i class="fas fa-cogs"></i>'), orderable=False)

    class Meta(TamerTableCommon.Meta):
        model = TamerPosition
