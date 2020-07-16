from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DetailView, DeleteView
import django_tables2 as tables
from tamer_app_contact.commons import TamerContactNoteCommon, TamerAppContactCommon
from tamer_app_contact.forms import TamerContactForm, TamerKindContactForm, TamerContactNoteForm
from tamer_app_contact.models import TamerContact, TamerKindContact, TamerContactNote
from tamer_app_contact.tables import TamerContactTable, TamerKindContactTable, TamerContactNoteTable


class TamerContactView(TamerAppContactCommon, tables.SingleTableView):
    template_name = 'view.html'
    model = TamerContact
    table_class = TamerContactTable
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['caption'] = 'Контакты'
        # context['table'] =
        return context


class TamerContactCreate(TamerAppContactCommon, CreateView):
    template_name = 'create-update.html'
    model = TamerContact
    form_class = TamerContactForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой записи контакта'
        return context


class TamerContactDetail(TamerAppContactCommon, DetailView):
    template_name = 'contact_detail.html'
    model = TamerContact

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Просмотр записи контакта'
        context['table'] = TamerContactNoteTable(TamerContactNote.objects.filter(contact=self.object))
        return context


class TamerContactUpdate(TamerAppContactCommon, UpdateView):
    template_name = 'create-update.html'
    model = TamerContact
    form_class = TamerContactForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Редактирование записи контакта'
        return context


class TamerContactDelete(TamerAppContactCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerContact
    success_url = reverse_lazy('tamer-contact-view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи контакта'
        return context


# End Contact


class TamerKindContactView(TamerAppContactCommon, tables.SingleTableView):
    template_name = 'view.html'
    model = TamerKindContact
    table_class = TamerKindContactTable
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['caption'] = 'Тип контактной информации'
        return context


class TamerKindContactCreate(TamerAppContactCommon, CreateView):
    template_name = 'create-update.html'
    model = TamerKindContact
    form_class = TamerKindContactForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой записи типа контактной информации'
        return context


class TamerKindContactDetail(TamerAppContactCommon, DetailView):
    template_name = 'detail.html'
    model = TamerKindContact

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Просмотр записи типа контактной информации'
        return context


class TamerKindContactUpdate(TamerAppContactCommon, UpdateView):
    template_name = 'create-update.html'
    model = TamerKindContact
    form_class = TamerKindContactForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Редактирование записи типа контактной информации'
        return context


class TamerKindContactDelete(TamerAppContactCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerKindContact
    success_url = reverse_lazy('tamer-kind-contact-view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи типа контактной информации'
        return context


class TamerContactNoteCreate(TamerContactNoteCommon, CreateView):
    template_name = 'create_contact_note.html'
    model = TamerContactNote
    form_class = TamerContactNoteForm
    contact_id = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой записи контактной информации'
        contact_path = self.request.GET.get('contact', 0)
        if contact_path != 0:
            self.contact_id = contact_path.strip('/').split('/')[-1]
            context['form'].fields['contact'].initial = TamerContact.objects.get(id=self.contact_id)
        return context


class TamerContactNoteDetail(TamerContactNoteCommon, DetailView):
    template_name = 'detail.html'
    model = TamerContactNote

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Просмотр записи контактной информации'
        context['parent_get_link'] = '/?contact=%s' % self.request.GET.get('contact', 0)
        context['parent_link'] = '/contact/%s' % self.request.GET.get('contact', 0)
        return context


class TamerContactNoteUpdate(TamerContactNoteCommon, UpdateView):
    template_name = 'create-update.html'
    model = TamerContactNote
    form_class = TamerContactNoteForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Редактирование записи контактной информации'
        contact_path = self.request.GET.get('contact', 0)
        if contact_path != 0:
            contact_id = contact_path.strip('/').split('/')[-1]
            context['form'].fields['contact'].initial = TamerContact.objects.get(id=contact_id)
            context['parent_link'] = '/contact/%s' % self.request.GET.get('contact', 0)
        return context


class TamerContactNoteDelete(TamerContactNoteCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerContactNote

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи контактной информации'
        return context
