from django.utils.safestring import mark_safe
from django_tables2.utils import A
import django_tables2 as tables

from tamer_app_base.tables import TamerTableCommon
from tamer_app_task.models import TamerTask


class TamerTaskTable(TamerTableCommon, tables.Table):
    id = tables.LinkColumn('tamer-task-update', args=[A('pk')])
    # subject = tables.LinkColumn('tamer-task-update', args=[A('pk')])
    subject = tables.TemplateColumn(
        '<a href="{% url "tamer-task-update" record.id %}">{{ record.subject }}</a><br>{{ record.description|safe }}')
    start = tables.TemplateColumn(
        '{{ record.start }}<br>{{ record.planning }}', verbose_name='Период')
    estimate = tables.TemplateColumn(
        '{{ record.estimate }}', verbose_name='Оценка')
    status = tables.TemplateColumn('{{ record.get_current_status }}{{ record.is_delay }}', verbose_name='Статус')
    actions = tables.TemplateColumn('{{ record.get_possible_actions_annotation }}', verbose_name='Действия')
    # remove1 = tables.LinkColumn('tamer-task-delete', args=[A('pk')],
    #                            verbose_name=mark_safe('<i class="fas fa-cogs"></i>'),
    #                            text=mark_safe('<i class="far fa-trash-alt"></i>'), orderable=False)
    #
    remove = tables.TemplateColumn(
        '<a onclick = "onclick_modal({{ record.id }}, \'{{ record.subject }}\')" class="far fa-trash-alt text-info"></a>',
        orderable=False, verbose_name=mark_safe('<i class="fas fa-cogs"></i>'))

    class Meta(TamerTableCommon.Meta):
        model = TamerTask
        exclude = ('description', 'planning', 'is_archive')
