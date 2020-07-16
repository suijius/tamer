from tamer_app_base.commons import TamerCommon


class TamerAppEmployeeCommon(TamerCommon):
    menu = {'menu': [{'title': 'Сотрудники', 'link': 'employee', 'sidebar_link': 'employee'},
                     {'title': 'Роли', 'link': 'position', 'sidebar_link': 'position'}]}

    title = 'Сотрудники'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.sidebar_link = 'employee'
        return context



# # Contact Note
# class TamerContactNoteCommon(TamerAppContactCommon):
#     def post(self, request, *args, **kwargs):
#         self.success_url = '/contact/%s' % request.GET.get('contact', 0)
#         return super().post(request, *args, **kwargs)
