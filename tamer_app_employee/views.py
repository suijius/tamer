from django.db.models import Max
from django.forms import DateTimeField
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DetailView, DeleteView
import django_tables2 as tables
from tamer_app_employee.commons import TamerAppEmployeeCommon#, TamerAppContactCommon
from tamer_app_employee.forms import TamerEmployeeForm, TamerPositionForm#, TamerKindContactForm
from tamer_app_employee.models import TamerEmployee, TamerPosition#, TamerKindContact
from tamer_app_employee.tables import TamerEmployeeTable, TamerPositionTable#, TamerKindContactTable
from django.db import connections
import datetime


class TamerEmployeeView(TamerAppEmployeeCommon, tables.SingleTableView):
    template_name = 'view.html'
    model = TamerEmployee
    table_class = TamerEmployeeTable
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['caption'] = 'Сотрудники'
        return context


class TamerEmployeeCreate(TamerAppEmployeeCommon, CreateView):
    template_name = 'create-update.html'
    model = TamerEmployee
    form_class = TamerEmployeeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой записи сотрудника'
        context['form'].fields['begin'].initial = datetime.datetime.now()
        context['form'].fields['end'].initial = datetime.datetime(2999, 12, 31, 0, 0, 0)
        return context

    def post(self, request, *args, **kwargs):
        te = TamerEmployee()
        te.id = TamerEmployee.objects.aggregate(Max('id'))['id__max']
        if te.id is None:
            te.id = 1
        else:
            te.id += 1
        te.position = TamerPosition.objects.get(id=request.POST.get('position', ''))
        te.begin = request.POST.get('begin', '')
        te.end = request.POST.get('end', '')
        te.name = request.POST.get('name', '')
        te.save(force_insert=True)
        return HttpResponseRedirect(reverse_lazy('tamer-employee-view'))


class TamerEmployeeDetail(TamerAppEmployeeCommon, DetailView):
    template_name = 'detail.html'
    model = TamerEmployee

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Просмотр записи сотрудника'
        context['table'] = TamerEmployeeTable(TamerEmployee.objects.filter(name=self.object))
        return context


class TamerEmployeeUpdate(TamerAppEmployeeCommon, UpdateView):
    template_name = 'create-update.html'
    model = TamerEmployee
    form_class = TamerEmployeeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Редактирование записи сотрудника'
        return context

    def post(self, request, *args, **kwargs):
        time2exchange = datetime.datetime.now()
        with connections['default'].cursor() as cursor:
            query = '''
                update tamer_employee set 
                    end = '%s'
                where
                    id = %s and
                    '%s' between begin and end
            ''' % (time2exchange, kwargs['pk'], time2exchange)
            print(query)
            cursor.execute(query)
            connections['default'].commit()

        te = TamerEmployee()
        te.id = kwargs['pk']
        te.position = TamerPosition.objects.get(id=request.POST.get('position', ''))
        te.begin = time2exchange
        te.end = datetime.datetime(2999, 12, 31, 0, 0, 0)
        te.name = request.POST.get('name', 0)
        te.save(force_insert=True)
        return HttpResponseRedirect(reverse_lazy('tamer-employee-view'))


class TamerEmployeeDelete(TamerAppEmployeeCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerEmployee
    success_url = reverse_lazy('tamer-employee-view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи сотрудника'
        return context

    def post(self, request, *args, **kwargs):
        time2exchange = datetime.datetime.now()
        with connections['default'].cursor() as cursor:
            query = '''
                update tamer_employee set 
                    end = '%s'
                where
                    id = %s and
                    '%s' between begin and end
            ''' % (time2exchange, kwargs['pk'], time2exchange)
            print(query)
            cursor.execute(query)
            connections['default'].commit()
        return HttpResponseRedirect(self.success_url)


class TamerPositionView(TamerAppEmployeeCommon, tables.SingleTableView):
    template_name = 'view.html'
    model = TamerPosition
    table_class = TamerPositionTable
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['caption'] = 'Проектные роли'
        return context


class TamerPositionCreate(TamerAppEmployeeCommon, CreateView):
    template_name = 'create-update.html'
    model = TamerPosition
    form_class = TamerPositionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Создание новой записи проектной роли'
        # context['form'].fields['begin'].initial = datetime.datetime.now()
        # context['form'].fields['end'].initial = datetime.datetime(2999, 12, 31, 0, 0, 0)
        return context

    # def post(self, request, *args, **kwargs):
    #     tp = TamerPosition()
    #     # tp.id = TamerPosition.objects.aggregate(Max('id'))['id__max'] + 1
    #     tp.position = request.POST.get('position', '')
    #     tp.begin = request.POST.get('begin', '')
    #     tp.end = request.POST.get('end', '')
    #     tp.rate = request.POST.get('rate', '')
    #     tp.save(force_insert=True)
    #     return HttpResponseRedirect(reverse_lazy('tamer-position-view'))


class TamerPositionDetail(TamerAppEmployeeCommon, DetailView):
    template_name = 'detail.html'
    model = TamerPosition

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Просмотр записи проектной роли'
        return context


class TamerPositionUpdate(TamerAppEmployeeCommon, UpdateView):
    template_name = 'create-update.html'
    model = TamerPosition
    form_class = TamerPositionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Редактирование записи проектной роли'
        return context

    # def post(self, request, *args, **kwargs):
    #     time2exchange = datetime.datetime.now()
    #     with connections['default'].cursor() as cursor:
    #         query = '''
    #             update tamer_position set
    #                 end = '%s'
    #             where
    #                 id = %s and
    #                 '%s' between begin and end
    #         ''' % (time2exchange, kwargs['pk'], time2exchange)
    #         print(query)
    #         cursor.execute(query)
    #         connections['default'].commit()
    #
    #     tp = TamerPosition()
    #     tp.id = kwargs['pk']
    #     tp.position = request.POST.get('position', '')
    #     begin = request.POST.get('begin', '')
    #     tp.begin = time2exchange
    #     if len(begin.split(' ')) == 1:
    #         tp.begin = begin
    #     end = request.POST.get('end', '')
    #     tp.end = datetime.datetime(2999, 12, 31, 0, 0, 0)
    #     if len(end.split(' ')) == 1:
    #         tp.end = end
    #     tp.rate = request.POST.get('rate', 0)
    #     tp.save(force_insert=True)
    #     return HttpResponseRedirect(reverse_lazy('tamer-position-view'))


class TamerPositionDelete(TamerAppEmployeeCommon, DeleteView):
    template_name = 'delete.html'
    model = TamerPosition
    success_url = reverse_lazy('tamer-position-view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Удаление записи проектной роли'
        return context

    def post(self, request, *args, **kwargs):
        time2exchange = datetime.datetime.now()
        with connections['default'].cursor() as cursor:
            query = '''
                update tamer_position set 
                    end = '%s'
                where
                    id = %s and
                    '%s' between begin and end
            ''' % (time2exchange, kwargs['pk'], time2exchange)
            print(query)
            cursor.execute(query)
            connections['default'].commit()
        return HttpResponseRedirect(self.success_url)

# class TamerContactNoteCreate(TamerContactNoteCommon, CreateView):
#     template_name = 'create_contact_note.html'
#     model = TamerContactNote
#     form_class = TamerContactNoteForm
#     contact_id = 0
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['label'] = 'Создание новой записи контактной информации'
#         contact_path = self.request.GET.get('contact', 0)
#         if contact_path != 0:
#             self.contact_id = contact_path.strip('/').split('/')[-1]
#             context['form'].fields['contact'].initial = TamerContact.objects.get(id=self.contact_id)
#         return context
#
#
# class TamerContactNoteDetail(TamerContactNoteCommon, DetailView):
#     template_name = 'detail.html'
#     model = TamerContactNote
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['label'] = 'Просмотр записи контактной информации'
#         context['parent_get_link'] = '/?contact=%s' % self.request.GET.get('contact', 0)
#         context['parent_link'] = '/contact/%s' % self.request.GET.get('contact', 0)
#         return context
#
#
# class TamerContactNoteUpdate(TamerContactNoteCommon, UpdateView):
#     template_name = 'create-update.html'
#     model = TamerContactNote
#     form_class = TamerContactNoteForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['label'] = 'Редактирование записи контактной информации'
#         contact_path = self.request.GET.get('contact', 0)
#         if contact_path != 0:
#             contact_id = contact_path.strip('/').split('/')[-1]
#             context['form'].fields['contact'].initial = TamerContact.objects.get(id=contact_id)
#         return context
#
#
# class TamerContactNoteDelete(TamerContactNoteCommon, DeleteView):
#     template_name = 'delete.html'
#     model = TamerContactNote
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['label'] = 'Удаление записи контактной информации'
#         return context
