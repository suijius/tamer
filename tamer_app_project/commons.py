from tamer_app_base.commons import TamerCommon


class TamerAppProjectCommon(TamerCommon):
    primary_menu = [{'title': 'Текущие проекты', 'link': '?project=open', 'sidebar_link': 'project'},
                     {'title': 'Закрытые проекты', 'link': '?project=close', 'sidebar_link': 'project'},
                     {'title': 'Пресейл', 'link': '?project=presale', 'sidebar_link': 'project'}]
    menu = {'menu': primary_menu}
    title = 'Проекты'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.sidebar_link = 'project'
        return context


class TamerPostCommon(TamerAppProjectCommon):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_get_link'] = '/?project=%s' % self.request.GET.get('project', 0)
        context['parent_link'] = '/project/%s' % self.request.GET.get('project', 0)
        return context

    def post(self, request, *args, **kwargs):
        self.success_url = '/project/%s' % request.GET.get('project', 0)
        return super().post(request, *args, **kwargs)


