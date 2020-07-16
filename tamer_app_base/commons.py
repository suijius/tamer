import copy


class TamerCommon:
    menu = {'menu': []}  # {'title': '', 'link': '', 'sidebar_link': ''}
    sidebar_link = ''
    foreign_fields = {'add_foreign_fields': []}  # 'add_foreign_fields': ['customer']
    title = ''
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.menu)
        context.update(self.foreign_fields)
        context['parent_get_link'] = ''
        context['parent_link'] = '..'
        context['delete_title'] = 'Вы точно хотите удалить - '
        context['delete_button_caption'] = 'Удалить'
        context['cancel_url'] = '../..'
        return context
