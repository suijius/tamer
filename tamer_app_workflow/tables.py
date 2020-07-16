import json
from json import JSONDecodeError

from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django_tables2.utils import A
import django_tables2 as tables

from tamer_app_base.tables import TamerTableCommon
from tamer_app_workflow.commons import TamerActionCommon
from tamer_app_workflow.models import TamerAction, TamerActionEdge, TamerEdge, TamerInstance, TamerObject, TamerState, TamerStateEdge, TamerWorkflow


class TamerWorkflowTable(TamerTableCommon, tables.Table):
    id = tables.LinkColumn('tamer-workflow-detail', args=[A('pk')])
    name = tables.LinkColumn('tamer-workflow-detail', args=[A('pk')])
    remove = tables.LinkColumn('tamer-workflow-delete', args=[A('pk')], verbose_name=mark_safe('<i class="fas fa-cogs"></i>'),
                               text=mark_safe('<i class="far fa-trash-alt"></i>'), orderable=False)

    class Meta(TamerTableCommon.Meta):
        model = TamerWorkflow


class TamerInstanceTable(TamerTableCommon, tables.Table):
    id = tables.LinkColumn('tamer-instance-detail', args=[A('pk')])
    name = tables.LinkColumn('tamer-instance-detail', args=[A('pk')])
    remove = tables.LinkColumn('tamer-instance-delete', args=[A('pk')], verbose_name=mark_safe('<i class="fas fa-cogs"></i>'),
                               text=mark_safe('<i class="far fa-trash-alt"></i>'), orderable=False)

    class Meta(TamerTableCommon.Meta):
        model = TamerInstance


class TamerActionTable(TamerTableCommon, tables.Table):
    id = tables.LinkColumn('tamer-action-update', args=[A('pk')])
    name = tables.LinkColumn('tamer-action-update', args=[A('pk')])
    remove = tables.LinkColumn('tamer-action-delete', args=[A('pk')], verbose_name=mark_safe('<i class="fas fa-cogs"></i>'),
                               text=mark_safe('<i class="far fa-trash-alt"></i>'), orderable=False)

    __functions = []

    class Meta(TamerTableCommon.Meta):
        model = TamerAction

    def render_function(self, value):
        if not len(self.__functions):
            self.__functions = TamerActionCommon.get_functions()
        value = [item[1] for item in self.__functions if item[0] == value][0].label
        return value


class TamerActionEdgeTable(TamerTableCommon, tables.Table):
    action = tables.TemplateColumn(
        '<a href="{% url "tamer-action-edge-update" record.id %}?edge={{ record.edge.id }}">{{ record.action.name }}</a>',
        verbose_name="Название")
    description = tables.TemplateColumn('{{ record.action.description }}', verbose_name="Описание")
    params = tables.TemplateColumn('{% load custom_tags %}{{ record.params | utf}}', verbose_name="Параметры")
    remove = tables.TemplateColumn('<a class="far fa-trash-alt" href="{% url "tamer-action-edge-delete" record.id %}?edge={{ view.object.id }}"></a>',
                                   verbose_name=mark_safe('<i class="fas fa-cogs"></i>'))

    class Meta(TamerTableCommon.Meta):
        model = TamerActionEdge
        fields = ('action', 'description', 'params')

    def render_params(self, value):
        params = {}
        try:
            params = json.loads(value)
        except JSONDecodeError:
            pass
        html = ''
        for key, value in params.items():
            html += '%s: %s<br/>' % (key, value)
        return html


class TamerStateTable(TamerTableCommon, tables.Table):
    id = tables.TemplateColumn('<a href="{% url "tamer-state-detail" record.id %}?workflow={{ view.object.id }}">{{ record.name }}</a>',
                               verbose_name="ID")
    name = tables.TemplateColumn('<a href="{% url "tamer-state-detail" record.id %}?workflow={{ view.object.id }}">{{ record.name }}</a>',
                                 verbose_name="Состояние")
    is_first = tables.TemplateColumn('<i class="fas fa-check" {% if not record.is_first %}hidden{% endif %}></i>')
    is_last = tables.TemplateColumn('<i class="fas fa-check" {% if not record.is_last %}hidden{% endif %}></i>')
    remove = tables.TemplateColumn('<a href="{% url "tamer-state-delete" record.id %}?workflow={{ view.object.id }}"><i class="far fa-trash-alt"></i></a>',
                                 verbose_name=mark_safe('<i class="fas fa-cogs"></i>'), orderable=False)

    class Meta(TamerTableCommon.Meta):
        model = TamerState
        exclude = ['active', 'workflow', 'id']


class TamerInactiveStateTable(TamerStateTable):
    remove = tables.TemplateColumn('<a href="{% url "tamer-state-delete" record.id %}?workflow={{ view.object.id }}"><i class="far fa-trash-alt"></i></a>',
                                 verbose_name=mark_safe('<i class="fas fa-cogs"></i>'), orderable=False)


class TamerStateEdgeTable(TamerTableCommon, tables.Table):
    edge = tables.TemplateColumn(
        '<a href="{% url "tamer-edge-detail" record.edge.id %}?workflow={{ record.edge.workflow.id }}">{{ record.edge.name }}</a>',
        verbose_name="Название")
    description = tables.TemplateColumn('{{ record.edge.description }}', verbose_name="Описание")
    state = tables.TemplateColumn('{{ record.edge.next_state.name }}', verbose_name="Следующее состояние")
    remove = tables.TemplateColumn('<a class="far fa-trash-alt" href="{% url "tamer-state-edge-delete" record.id %}?state={{ view.object.id }}"></a>',
                                   verbose_name=mark_safe('<i class="fas fa-cogs"></i>'))

    class Meta(TamerTableCommon.Meta):
        model = TamerStateEdge
        fields = ('edge', 'description', 'state')


class TamerObjectTable(TamerTableCommon, tables.Table):
    id = tables.LinkColumn('tamer-object-update', args=[A('pk')])
    name = tables.LinkColumn('tamer-object-update', args=[A('pk')])
    remove = tables.LinkColumn('tamer-object-delete', args=[A('pk')], verbose_name=mark_safe('<i class="fas fa-cogs"></i>'),
                               text=mark_safe('<i class="far fa-trash-alt"></i>'), orderable=False)

    class Meta(TamerTableCommon.Meta):
        model = TamerObject


class TamerEdgeTable(TamerTableCommon, tables.Table):
    id = tables.LinkColumn('tamer-edge-detail', args=[A('pk')])
    name = tables.LinkColumn('tamer-edge-detail', args=[A('pk')])
    remove = tables.TemplateColumn('<a href="{% url "tamer-edge-delete" record.id %}?workflow={{ view.object.id }}"><i class="far fa-trash-alt"></i></a>',
                                 verbose_name=mark_safe('<i class="fas fa-cogs"></i>'), orderable=False)

    class Meta(TamerTableCommon.Meta):
        model = TamerEdge
        exclude = ['active', 'workflow', 'id']


class TamerInactiveEdgeTable(TamerEdgeTable):
    remove = tables.TemplateColumn('<a href="{% url "tamer-edge-delete" record.id %}?workflow={{ view.object.id }}"><i class="far fa-trash-alt"></i></a>',
                                 verbose_name=mark_safe('<i class="fas fa-cogs"></i>'), orderable=False)
