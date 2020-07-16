import copy

from django.urls import reverse_lazy
import django_tables2 as tables
from django.views.generic import UpdateView, CreateView, DetailView, DeleteView

from tamer_app_project.commons import TamerAppProjectCommon, TamerPostCommon
from tamer_app_project.forms import TamerProjectForm, TamerStageForm, TamerBusinessTripForm, TamerEducationForm, \
    TamerEquipmentForm, \
    TamerSubcontractForm
from tamer_app_project.models import TamerProject, TamerStage, TamerBusinessTrip, TamerEducation, TamerEquipment, \
    TamerSubcontract
from tamer_app_project.tables import TamerProjectTable, TamerStageTable, TamerSubcontractTable, TamerBusinessTripTable, \
    TamerEducationTable, \
    TamerEquipmentTable


class TamerProjectView(TamerAppProjectCommon, tables.SingleTableView):
    template_name = 'view.html'
    model = TamerProject
    table_class = TamerProjectTable
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['caption'] = 'Текущие проекты'
        return context


class TamerProjectCreate(TamerAppProjectCommon, CreateView):
    template_name = 'create-update.html'
    model = TamerProject
    form_class = TamerProjectForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой записи проекта'
        return context


class TamerProjectDetail(TamerAppProjectCommon, DetailView):
    template_name = 'project_detail.html'
    model = TamerProject

    def get_context_data(self, **kwargs):
        if self.request.GET.get('section', '') != '':
            self.template_name = 'detail.html'

        context = super().get_context_data(**kwargs)
        context['label'] = self.object.subject  # 'Просмотр записи проекта'
        stage_sort = False
        subcontract_sort = False
        equipment_sort = False
        education_sort = False
        business_trip_sort = False
        for sort in self.request.GET:
            if 'stage-' in sort:
                context['stage_table'] = TamerStageTable(
                    TamerStage.objects.filter(project=self.object).order_by(self.request.GET[sort]))
                stage_sort = True
            if 'subcontract-' in sort:
                context['subcontract_table'] = TamerSubcontractTable(
                    TamerSubcontract.objects.filter(project=self.object).order_by(self.request.GET[sort]))
                subcontract_sort = True
            if 'equipment-' in sort:
                context['equipment_table'] = TamerEquipmentTable(
                    TamerEquipment.objects.filter(project=self.object).order_by(self.request.GET[sort]))
                equipment_sort = True
            if 'education-' in sort:
                context['education_table'] = TamerEducationTable(
                    TamerEducation.objects.filter(project=self.object).order_by(self.request.GET[sort]))
                education_sort = True
            if 'business-trip-' in sort:
                context['business_trip_table'] = TamerBusinessTripTable(
                    TamerBusinessTrip.objects.filter(project=self.object).order_by(self.request.GET[sort]))
                business_trip_sort = True
        if not stage_sort:
            context['stage_table'] = TamerStageTable(TamerStage.objects.filter(project=self.object))
        if not subcontract_sort:
            context['subcontract_table'] = TamerSubcontractTable(TamerSubcontract.objects.filter(project=self.object))
        if not equipment_sort:
            context['equipment_table'] = TamerEquipmentTable(TamerEquipment.objects.filter(project=self.object))
        if not education_sort:
            context['education_table'] = TamerEducationTable(TamerEducation.objects.filter(project=self.object))
        if not business_trip_sort:
            context['business_trip_table'] = TamerBusinessTripTable(
                TamerBusinessTrip.objects.filter(project=self.object))

        self.menu = {'menu': []}
        self.menu['menu'].append({'title': self.object.subject,
                                  'subnav': [{'title': 'Титульная информация о проекте', 'link': '.'},
                                             {'title': 'Документы', 'link': '?section=doc'},
                                             {'title': 'Задачи', 'link': '?section=task'},
                                             {'title': 'Требования', 'link': '?section=requirement'},
                                             {'title': 'Контакты', 'link': '?section=contact'},
                                             {'title': 'Персонал', 'link': '?section=employee'},
                                             {'title': 'Риски', 'link': '?section=risk'}
                                             ]})
        self.menu['menu'] += copy.deepcopy((self.primary_menu))
        return context


class TamerProjectUpdate(TamerAppProjectCommon, UpdateView):
    template_name = 'create-update.html'
    model = TamerProject
    form_class = TamerProjectForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Редактирование записи проекта'
        return context


class TamerProjectDelete(TamerAppProjectCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerProject
    success_url = reverse_lazy('tamer-project-view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи проекта'
        return context


class TamerStageCreate(TamerPostCommon, CreateView):
    template_name = 'create-update.html'
    model = TamerStage
    form_class = TamerStageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой записи этапа'
        path = self.request.GET.get('project', 0)
        if path != 0:
            item_id = path.strip('/').split('/')[-1]
            context['form'].fields['project'].initial = TamerProject.objects.get(id=item_id)
        return context


class TamerStageDetail(TamerPostCommon, DetailView):
    template_name = 'detail.html'
    model = TamerStage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Просмотр записи проекта'
        return context


class TamerStageUpdate(TamerPostCommon, UpdateView):
    template_name = 'create-update.html'
    model = TamerStage
    form_class = TamerStageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Редактирование записи этапа'
        return context


class TamerStageDelete(TamerPostCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerStage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи проекта'
        return context


class TamerSubcontractCreate(TamerPostCommon, CreateView):
    template_name = 'create-update.html'
    model = TamerSubcontract
    form_class = TamerSubcontractForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой записи подрядных работ'
        path = self.request.GET.get('project', 0)
        if path != 0:
            item_id = path.strip('/').split('/')[-1]
            context['form'].fields['project'].initial = TamerProject.objects.get(id=item_id)
        return context


class TamerSubcontractDetail(TamerPostCommon, DetailView):
    template_name = 'detail.html'
    model = TamerSubcontract

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Просмотр записи подрядных работ'
        return context


class TamerSubcontractUpdate(TamerPostCommon, UpdateView):
    template_name = 'create-update.html'
    model = TamerSubcontract
    form_class = TamerSubcontractForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Редактирование записи подрядных работ'
        return context


class TamerSubcontractDelete(TamerPostCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerSubcontract

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи подрядных работ'
        return context


class TamerEducationCreate(TamerPostCommon, CreateView):
    template_name = 'create-update.html'
    model = TamerEducation
    form_class = TamerEducationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой записи обучения'
        path = self.request.GET.get('project', 0)
        if path != 0:
            item_id = path.strip('/').split('/')[-1]
            context['form'].fields['project'].initial = TamerProject.objects.get(id=item_id)
        return context


class TamerEducationDetail(TamerPostCommon, DetailView):
    template_name = 'detail.html'
    model = TamerEducation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Просмотр записи обучения'
        return context


class TamerEducationUpdate(TamerPostCommon, UpdateView):
    template_name = 'create-update.html'
    model = TamerEducation
    form_class = TamerEducationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Редактирование записи обучения'
        return context


class TamerEducationDelete(TamerPostCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerEducation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи обучения'
        return context


class TamerEquipmentCreate(TamerPostCommon, CreateView):
    template_name = 'create-update.html'
    model = TamerEquipment
    form_class = TamerEquipmentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой записи поставок оборудования'
        path = self.request.GET.get('project', 0)
        if path != 0:
            item_id = path.strip('/').split('/')[-1]
            context['form'].fields['project'].initial = TamerProject.objects.get(id=item_id)
        return context


class TamerEquipmentDetail(TamerPostCommon, DetailView):
    template_name = 'detail.html'
    model = TamerEquipment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Просмотр записи поставок оборудования'
        return context


class TamerEquipmentUpdate(TamerPostCommon, UpdateView):
    template_name = 'create-update.html'
    model = TamerEquipment
    form_class = TamerEquipmentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Редактирование записи поставок оборудования'
        return context


class TamerEquipmentDelete(TamerPostCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerEquipment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи поставок оборудования'
        return context


class TamerBusinessTripCreate(TamerPostCommon, CreateView):
    template_name = 'create-update.html'
    model = TamerBusinessTrip
    form_class = TamerBusinessTripForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой записи командрировки'
        path = self.request.GET.get('project', 0)
        if path != 0:
            item_id = path.strip('/').split('/')[-1]
            context['form'].fields['project'].initial = TamerProject.objects.get(id=item_id)
        return context


class TamerBusinessTripDetail(TamerPostCommon, DetailView):
    template_name = 'detail.html'
    model = TamerBusinessTrip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Просмотр записи командрировки'
        return context


class TamerBusinessTripUpdate(TamerPostCommon, UpdateView):
    template_name = 'create-update.html'
    model = TamerBusinessTrip
    form_class = TamerBusinessTripForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Редактирование записи командрировки'
        return context


class TamerBusinessTripDelete(TamerPostCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerBusinessTrip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи командрировки'
        return context
