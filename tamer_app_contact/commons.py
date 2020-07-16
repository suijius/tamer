from tamer_app_base.commons import TamerCommon


class TamerAppContactCommon(TamerCommon):
    menu = {'menu': [{'title': 'Контакты', 'link': 'contact', 'sidebar_link': 'contact'},
                     {'title': 'Тип контактной информации', 'link': 'kind_contact', 'sidebar_link': 'contact'}]}

    title = 'Контакты'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.sidebar_link = 'contact'
        return context


# Contact Note
class TamerContactNoteCommon(TamerAppContactCommon):
    def post(self, request, *args, **kwargs):
        self.success_url = '/contact/%s' % request.GET.get('contact', 0)
        return super().post(request, *args, **kwargs)
