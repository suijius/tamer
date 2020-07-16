import copy

from django.db import connections
from django.db.models import Max, Count


from tamer_app_base.commons import TamerCommon
from tamer_app_task.models import TamerTask
from tamer_app_workflow.models import TamerInstance


class TamerAppTaskCommon(TamerCommon):
    primary_menu = [{'title': 'Активные задачи', 'link': '/task', 'sidebar_link': 'task'},
                    {'title': 'Архив задач', 'link': '?is_archive=True', 'sidebar_link': 'task'}]
    # {'title': 'Задачки', 'sidebar_link': 'task',
    #  'subnav': [{'title': 'Задачи 1', 'link': 'task'}, {'title': 'Задачи 2', 'link': 'task'}]}]
    menu = {'menu': []}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.sidebar_link = 'task'
        self.title = 'Задачи'
        query_type = '''SELECT w.id, w.name, count(*) as c
FROM tamer_instance as i
join tamer_task as t on i.object_id = t.id and t.is_archive=0
join tamer_state as s on i.state_id = s.id
join tamer_workflow as w on s.workflow_id = w.id
where object_type_id = 2
group by workflow_id
order by c desc
        '''
        with connections['default'].cursor() as cursor:
            cursor.execute(query_type)
            submenu = [{'title': item[1], 'link': '?workflow=%s' % item[0]} for item in cursor.fetchall()]
            self.menu = {'menu':[]}
            if 'object' in dir(self) and self.object is not None:
                self.menu['menu'].append({'title': self.object.subject, 'link': '.'})
            self.menu['menu'].append({'title': 'Задачи по типам', 'sidebar_link': 'task', 'submenu':[]})
            self.menu['menu'][-1]['submenu'] = submenu

            self.menu['menu'].append({'title': 'Задачи по состоянию', 'sidebar_link': 'task', 'submenu':[
                {'title': 'Новые', 'link': '?state=0'},
                {'title': 'Открытые', 'link': '?state=1'},
                {'title': 'Закрытые', 'link': '?state=2'},
            ]})
            self.menu['menu'] += copy.deepcopy((self.primary_menu))
        return context

    def post(self, request, *args, **kwargs):
        self.success_url = '/task/%s' % request.GET.get('task', "")
        return super().post(request, *args, **kwargs)