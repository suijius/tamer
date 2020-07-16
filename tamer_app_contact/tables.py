from django.utils.safestring import mark_safe
from django_tables2 import A
import django_tables2 as tables

from tamer_app_base.tables import TamerTableCommon
from tamer_app_contact.models import TamerContact, TamerKindContact, TamerContactNote


class TamerContactTable(TamerTableCommon, tables.Table):
    id = tables.LinkColumn('tamer-contact-detail', args=[A('pk')])
    name = tables.LinkColumn('tamer-contact-detail', args=[A('pk')])
    note = tables.TemplateColumn('<a class="row">{{ record.note }}</a>', verbose_name='Контактные данные')
    remove = tables.LinkColumn('tamer-contact-delete', args=[A('pk')], verbose_name=mark_safe('<i class="fas fa-cogs"></i>'),
                               text=mark_safe('<i class="far fa-trash-alt"></i>'), orderable=False)

    class Meta(TamerTableCommon.Meta):
        model = TamerContact


class TamerKindContactTable(TamerTableCommon, tables.Table):
    id = tables.LinkColumn('tamer-kind-contact-detail', args=[A('pk')])
    name = tables.LinkColumn('tamer-kind-contact-detail', args=[A('pk')])
    remove = tables.LinkColumn('tamer-kind-contact-delete', args=[A('pk')], verbose_name=mark_safe('<i class="fas fa-cogs"></i>'),
                               text=mark_safe('<i class="far fa-trash-alt"></i>'), orderable=False)

    class Meta(TamerTableCommon.Meta):
        model = TamerKindContact


class TamerContactNoteTable(TamerTableCommon, tables.Table):
    id = tables.TemplateColumn('<a href="{% url "tamer-contact-note-update" record.id %}?contact={{ view.object.id }}">{{ record.id }}</a>')
    contact = tables.Column(visible=False)
    note = tables.TemplateColumn('<a href="{% url "tamer-contact-note-update" record.id %}?contact={{ view.object.id }}">{{ record.note }}</a>')
    remove = tables.TemplateColumn('<a class="far fa-trash-alt" href="{% url "tamer-contact-note-delete" record.id %}?contact={{ view.object.id }}">'
                                   '</a>', verbose_name=mark_safe('<i class="fas fa-cogs"></i>'), orderable=False)

    class Meta(TamerTableCommon.Meta):
        model = TamerContactNote
