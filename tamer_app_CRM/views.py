from django.urls import reverse_lazy
import django_tables2 as tables
from django.views.generic import UpdateView, CreateView, DetailView, DeleteView

from tamer_app_CRM.commons import TamerOpportunityCommon, TamerContractCommon, TamerAppCRMCommon, TamerCustomerCommon
from tamer_app_CRM.forms import TamerCustomerForm, TamerOpportunityForm, TamerContractForm, TamerOpportunityContactForm
from tamer_app_CRM.models import TamerOpportunity, TamerCustomer, TamerContract, TamerOpportunityContact
from tamer_app_CRM.tables import TamerCustomerTable, TamerOpportunityTable, TamerContractTable, TamerOpportunityContactTable


class TamerCustomerView(TamerAppCRMCommon, tables.SingleTableView):
    template_name = 'view.html'
    model = TamerCustomer
    table_class = TamerCustomerTable
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['caption'] = 'Заказчики'
        return context


class TamerCustomerCreate(TamerCustomerCommon, CreateView):
    template_name = 'create-update.html'
    model = TamerCustomer
    form_class = TamerCustomerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой записи заказчика'
        return context


class TamerCustomerDetail(TamerCustomerCommon, DetailView):
    template_name = 'detail.html'
    model = TamerCustomer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Просмотр записи заказчика'
        return context


class TamerCustomerUpdate(TamerCustomerCommon, UpdateView):
    template_name = 'create-update.html'
    model = TamerCustomer
    form_class = TamerCustomerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Редактирование записи заказчика'
        return context


class TamerCustomerDelete(TamerCustomerCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerCustomer
    success_url = reverse_lazy('tamer-customer-view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи заказчика'
        return context


class TamerOpportunityView(TamerOpportunityCommon, tables.SingleTableView):
    template_name = 'view.html'
    model = TamerOpportunity
    table_class = TamerOpportunityTable
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['caption'] = 'Возможности'
        return context


class TamerOpportunityCreate(TamerOpportunityCommon, CreateView):
    template_name = 'create-update.html'
    model = TamerOpportunity
    form_class = TamerOpportunityForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой записи возможности'
        return context


class TamerOpportunityDetail(TamerOpportunityCommon, DetailView):
    template_name = 'opportunity_detail.html'
    model = TamerOpportunity

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Просмотр записи возможности'
        context['table'] = TamerOpportunityContactTable(TamerOpportunityContact.objects.all())
        return context


class TamerOpportunityUpdate(TamerOpportunityCommon, UpdateView):
    template_name = 'create-update.html'
    model = TamerOpportunity
    form_class = TamerOpportunityForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Редактирование записи возможности'
        return context


class TamerOpportunityDelete(TamerAppCRMCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerOpportunity
    success_url = reverse_lazy('tamer-opportunity-view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи возможности'
        return context


class TamerContractView(TamerContractCommon, tables.SingleTableView):
    template_name = 'view.html'
    model = TamerContract
    table_class = TamerContractTable
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['caption'] = 'Договоры'
        return context


class TamerContractCreate(TamerContractCommon, CreateView):
    template_name = 'create-update.html'
    model = TamerContract
    form_class = TamerContractForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой записи договора'
        return context


class TamerContractDetail(TamerContractCommon, DetailView):
    template_name = 'detail.html'
    model = TamerContract

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Просмотр записи договора'
        return context


class TamerContractUpdate(TamerContractCommon, UpdateView):
    template_name = 'create-update.html'
    model = TamerContract
    form_class = TamerContractForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Редактирование записи договора'
        return context


class TamerContractDelete(TamerAppCRMCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerContract
    success_url = reverse_lazy('tamer-contract-view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи договора'
        return context


class TamerOpportunityContactCreate(TamerAppCRMCommon, CreateView):
    template_name = 'create-update.html'
    model = TamerOpportunityContact
    form_class = TamerOpportunityContactForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Новый контакт для возможности'
        opportunity_path = self.request.GET.get('opportunity', 0)
        if opportunity_path != 0:
            opportunity_id = opportunity_path.strip('/').split('/')[-1]
            context['form'].fields['opportunity'].initial = TamerOpportunity.objects.get(id=opportunity_id)
        return context


class TamerOpportunityContactUpdate(TamerAppCRMCommon, UpdateView):
    template_name = 'create-update.html'
    model = TamerOpportunityContact
    form_class = TamerOpportunityContactForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Редактирование записи контакта для возможности'
        return context


class TamerOpportunityContactDelete(TamerAppCRMCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerOpportunityContact

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи контакта из возможности'
        return context
