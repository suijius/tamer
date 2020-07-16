from django.utils.safestring import mark_safe
from django_tables2.utils import A
import django_tables2 as tables

from tamer_app_CRM.models import TamerCustomer, TamerOpportunity, TamerContract, TamerOpportunityContact
from tamer_app_base.tables import TamerTableCommon


class TamerCustomerTable(TamerTableCommon, tables.Table):
    id = tables.LinkColumn('tamer-customer-detail', args=[A('pk')])
    name = tables.LinkColumn('tamer-customer-detail', args=[A('pk')])
    remove = tables.LinkColumn('tamer-customer-delete', args=[A('pk')], verbose_name=mark_safe('<i class="fas fa-cogs"></i>'),
                               text=mark_safe('<i class="far fa-trash-alt"></i>'), orderable=False)

    class Meta(TamerTableCommon.Meta):
        model = TamerCustomer


class TamerOpportunityTable(TamerTableCommon, tables.Table):
    id = tables.LinkColumn('tamer-opportunity-detail', args=[A('pk')])
    subject = tables.LinkColumn('tamer-opportunity-detail', args=[A('pk')])
    remove = tables.LinkColumn('tamer-opportunity-delete', args=[A('pk')], verbose_name=mark_safe('<i class="fas fa-cogs"></i>'),
                               text=mark_safe('<i class="far fa-trash-alt"></i>'), orderable=False)

    class Meta(TamerTableCommon.Meta):
        model = TamerOpportunity


class TamerContractTable(TamerTableCommon, tables.Table):
    id = tables.LinkColumn('tamer-contract-detail', args=[A('pk')])
    contract = tables.LinkColumn('tamer-contract-detail', args=[A('pk')])
    remove = tables.LinkColumn('tamer-contract-delete', args=[A('pk')], verbose_name=mark_safe('<i class="fas fa-cogs"></i>'),
                               text=mark_safe('<i class="far fa-trash-alt"></i>'), orderable=False)

    class Meta(TamerTableCommon.Meta):
        model = TamerContract


class TamerOpportunityContactTable(TamerTableCommon, tables.Table):
    contact = tables.TemplateColumn(
        '<a href="{% url "tamer-opportunity-contact-update" record.id %}?opportunity={{ view.object.id }}">{{ record.contact }}</a>')
    contact_description = tables.TemplateColumn(
        '<a href="{% url "tamer-opportunity-contact-update" record.id %}?opportunity={{ view.object.id }}">{{ record.contact.description }}</a>',
        verbose_name='Описание к контакту')
    remove = tables.TemplateColumn(
        '<a class="far fa-trash-alt" href="{% url "tamer-opportunity-contact-delete" record.id %}?opportunity={{ view.object.id }}">'
        '</a>', verbose_name=mark_safe('<i class="fas fa-cogs"></i>'), orderable=False)

    class Meta(TamerTableCommon.Meta):
        model = TamerOpportunityContact
        exclude = ('opportunity',)
