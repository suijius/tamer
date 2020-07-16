import copy

from tamer_app_base.commons import TamerCommon


class TamerAppDocumentCommon(TamerCommon):
    primary_menu = [{'title': 'Шаблоны документов', 'link': '/document_template', 'sidebar_link': 'document'},
                    {'title': 'Документы', 'link': '/document', 'sidebar_link': 'document'}]

    menu = {'menu': primary_menu}
    title = 'Документы'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.sidebar_link = 'document'
        return context


class TamerDocumentCommon(TamerAppDocumentCommon):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.menu = {'menu': []}
        if 'object' in dir(self):
            self.menu['menu'].append({'title': self.object.name, 'link': '.'})
        self.menu['menu'] += copy.deepcopy((self.primary_menu))
        return context


class TamerDocumentTemplateCommon(TamerAppDocumentCommon):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.menu = {'menu': []}
        if 'object' in dir(self):
            self.menu['menu'].append({'title': self.object.type, 'link': '.'})
        self.menu['menu'] += copy.deepcopy((self.primary_menu))
        return context


class TamerDocumentTemplateSectionCommon(TamerAppDocumentCommon):
    def post(self, request, *args, **kwargs):
        self.success_url = '/document_template/%s' % request.GET.get('document_template', 0)
        return super().post(request, *args, **kwargs)


class TamerDocumentSectionCommon(TamerAppDocumentCommon):
    def post(self, request, *args, **kwargs):
        self.success_url = '/document/%s' % request.GET.get('document', 0)
        return super().post(request, *args, **kwargs)
