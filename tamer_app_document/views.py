import copy

import django_tables2 as tables
from django.db.models import Subquery, Exists
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, View

from tamer_app_document.commons import TamerAppDocumentCommon, TamerDocumentTemplateSectionCommon, \
    TamerDocumentSectionCommon, TamerDocumentCommon, TamerDocumentTemplateCommon
from tamer_app_document.forms import TamerDocumentTemplateForm, TamerDocumentTemplateSectionForm, TamerDocumentForm, \
    TamerDocumentSectionUpdateForm, TamerDocumentSectionCreateForm
from tamer_app_document.models import TamerDocumentTemplate, TamerDocumentTemplateSection, TamerDocument, \
    TamerDocumentSection
from tamer_app_document.tables import TamerDocumentTemplateTable, TamerDocumentTemplateSectionTable, \
    TamerDocumentTable, TamerDocumentSectionTable


class TamerDocumentTemplateView(TamerAppDocumentCommon, tables.SingleTableView):
    template_name = 'view.html'
    model = TamerDocumentTemplate
    table_class = TamerDocumentTemplateTable
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['caption'] = 'Шаблоны документов'
        return context


class TamerDocumentTemplateCreate(TamerAppDocumentCommon, CreateView):
    template_name = 'create-update.html'
    model = TamerDocumentTemplate
    form_class = TamerDocumentTemplateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой записи типа документа'
        return context


class TamerDocumentTemplateDetail(TamerDocumentTemplateCommon, DetailView):
    template_name = 'document_template_detail.html'
    model = TamerDocumentTemplate

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Просмотр записи шаблона документа'
        context['table'] = TamerDocumentTemplateSectionTable(
            TamerDocumentTemplateSection.objects.filter(document_template=self.object).order_by('sort'))
        return context


class TamerDocumentTemplateUpdate(TamerDocumentTemplateCommon, UpdateView):
    template_name = 'create-update.html'
    model = TamerDocumentTemplate
    form_class = TamerDocumentTemplateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Редактирование записи шаблона документа'
        return context


class TamerDocumentTemplateDelete(TamerDocumentTemplateCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerDocumentTemplate
    success_url = reverse_lazy('tamer-document-tempalate-view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи шаблона документа'
        return context


class TamerDocumentTemplateSectionCreate(TamerDocumentTemplateSectionCommon, CreateView):
    template_name = 'create-update.html'
    model = TamerDocumentTemplateSection
    form_class = TamerDocumentTemplateSectionForm
    document_template_id = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой записи раздела документа'
        document_template_path = self.request.GET.get('document_template', 0)
        if document_template_path != 0:
            self.document_template_id = document_template_path.strip('/').split('/')[-1]
            context['form'].fields['document_template'].initial = TamerDocumentTemplate.objects.get(
                id=self.document_template_id)
        return context


class TamerDocumentTemplateSectionUpdate(TamerDocumentTemplateSectionCommon, UpdateView):
    template_name = 'create-update.html'
    model = TamerDocumentTemplateSection
    form_class = TamerDocumentTemplateSectionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Редактирование записи раздела документа'
        document_template_path = self.request.GET.get('document_template', 0)
        if document_template_path != 0:
            document_template_id = document_template_path.strip('/').split('/')[-1]
            context['form'].fields['document_template'].initial = TamerDocumentTemplate.objects.get(
                id=document_template_id)
            context['parent_link'] = '/document_template/%s' % self.request.GET.get('document_template', 0)
        return context


class TamerDocumentTemplateSectionDelete(TamerDocumentTemplateSectionCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerDocumentTemplateSection

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи раздела документа'
        return context


class TamerDocumentView(TamerAppDocumentCommon, tables.SingleTableView):
    template_name = 'view.html'
    model = TamerDocument
    table_class = TamerDocumentTable
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['caption'] = 'Документы'
        return context


class TamerDocumentCreate(TamerAppDocumentCommon, CreateView):
    template_name = 'create-update.html'
    model = TamerDocument
    form_class = TamerDocumentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой записи документа'
        return context


class TamerDocumentDetail(TamerDocumentCommon, DetailView):
    template_name = 'document_detail.html'
    model = TamerDocument

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Просмотр записи шаблона документа'
        context['section_list'] = TamerDocumentSection.objects.filter(document=self.object).order_by('sort')
        return context


class TamerDocumentUpdate(TamerDocumentCommon, UpdateView):
    template_name = 'create-update.html'
    model = TamerDocument
    form_class = TamerDocumentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Редактирование записи документа'
        return context


class TamerDocumentDelete(TamerDocumentCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerDocument
    success_url = reverse_lazy('tamer-document-view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи документа'
        return context


class TamerDocumentSectionCreate(TamerDocumentSectionCommon, CreateView):
    template_name = 'create_document_section.html'
    model = TamerDocumentSection
    form_class = TamerDocumentSectionCreateForm
    document_id = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой записи раздела документа'
        document_path = self.request.GET.get('document', 0)
        if document_path != 0:
            self.document_id = document_path.strip('/').split('/')[-1]
            context['form'].fields['document'].initial = TamerDocument.objects.get(
                id=self.document_id)
        return context


class TamerDocumentSectionApplyTemplate(TamerAppDocumentCommon, View):
    def get(self, request, *args, **kwargs):
        # context = super().get_context_data(**kwargs)
        document_path = self.request.GET.get('document', 0)
        if document_path != 0:
            document_id = document_path.strip('/').split('/')[-1]
            document = TamerDocument.objects.get(id=document_id)
            document_section_list = TamerDocumentSection.objects.filter(document=document)
            document_template_section_list = TamerDocumentTemplateSection.objects.filter(document_template=document.document_template).exclude(
                section__in=Subquery(document_section_list.values('section')))
            for template_section in document_template_section_list:
                document_section = TamerDocumentSection()
                document_section.document = document
                document_section.sort = template_section.sort
                document_section.section = template_section.section
                document_section.description = template_section.description
                document_section.save(force_insert=True)
        return HttpResponseRedirect(reverse('tamer-document-detail', args=[document_id]))


class TamerDocumentSectionUpdate(TamerDocumentSectionCommon, UpdateView):
    template_name = 'document_create-update.html'
    model = TamerDocumentSection
    form_class = TamerDocumentSectionUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Редактирование записи раздела документа'
        document_path = self.request.GET.get('document', 0)
        if document_path != 0:
            document_id = document_path.strip('/').split('/')[-1]
            context['form'].fields['document'].initial = TamerDocument.objects.get(
                id=document_id)
            context['parent_link'] = '/document/%s' % self.request.GET.get('document', 0)
        return context


class TamerDocumentSectionDelete(TamerDocumentSectionCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerDocumentSection

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи раздела документа'
        return context
