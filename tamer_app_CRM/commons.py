from django.urls import reverse_lazy

from tamer_app_base.commons import TamerCommon

app_menu = {'menu': [{'title': 'Возможности', 'link': 'opportunity', 'sidebar_link': 'opportunity'},
                     {'title': 'Заказчики', 'link': 'customer', 'sidebar_link': 'opportunity'},
                     {'title': 'Договоры', 'link': 'contract', 'sidebar_link': 'opportunity'}]}

class TamerAppCRMCommon(TamerCommon):
    menu = app_menu
    title = 'CRM'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.sidebar_link = 'opportunity'
        return context

    def post(self, request, *args, **kwargs):
        self.success_url = '/opportunity/%s' % request.GET.get('opportunity', '')
        return super().post(request, *args, **kwargs)


class TamerCustomerCommon(TamerCommon):
    menu = app_menu

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.sidebar_link = 'opportunity'
        return context

    def post(self, request, *args, **kwargs):
        self.success_url = reverse_lazy('tamer-customer-view')
        return super().post(request, *args, **kwargs)

# Opportunity
class TamerOpportunityCommon(TamerAppCRMCommon):
    foreign_fields = {'add_foreign_fields': ['customer']}


# Contract
class TamerContractCommon(TamerAppCRMCommon):
    foreign_fields = {'add_foreign_fields': ['customer']}
