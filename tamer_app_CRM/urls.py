"""tamer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from tamer_app_CRM.views import TamerOpportunityUpdate, TamerOpportunityCreate, TamerCustomerCreate, TamerCustomerUpdate, \
    TamerCustomerView, TamerOpportunityView, TamerOpportunityDetail, TamerOpportunityDelete, TamerCustomerDetail, TamerCustomerDelete, \
    TamerContractView, TamerContractCreate, TamerContractDetail, TamerContractUpdate, TamerContractDelete, TamerOpportunityContactCreate, \
    TamerOpportunityContactDelete, TamerOpportunityContactUpdate

urlpatterns = [
    path('customer/', TamerCustomerView.as_view(), name='tamer-customer-view'),
    path('customer/create/', TamerCustomerCreate.as_view(), name='tamer-customer-create'),
    path('customer/<int:pk>/', TamerCustomerDetail.as_view(), name='tamer-customer-detail'),
    path('customer/<int:pk>/update/', TamerCustomerUpdate.as_view(), name='tamer-customer-update'),
    path('customer/<int:pk>/delete/', TamerCustomerDelete.as_view(), name='tamer-customer-delete'),

    path('opportunity/', TamerOpportunityView.as_view(), name='tamer-opportunity-view'),
    path('opportunity/create/', TamerOpportunityCreate.as_view(), name='tamer-opportunity-create'),
    path('opportunity/<int:pk>/', TamerOpportunityDetail.as_view(), name='tamer-opportunity-detail'),
    path('opportunity/<int:pk>/update/', TamerOpportunityUpdate.as_view(), name='tamer-opportunity-update'),
    path('opportunity/<int:pk>/delete/', TamerOpportunityDelete.as_view(), name='tamer-opportunity-delete'),

    path('contract/', TamerContractView.as_view(), name='tamer-contract-view'),
    path('contract/create/', TamerContractCreate.as_view(), name='tamer-contract-create'),
    path('contract/<int:pk>/', TamerContractDetail.as_view(), name='tamer-contract-detail'),
    path('contract/<int:pk>/update/', TamerContractUpdate.as_view(), name='tamer-contract-update'),
    path('contract/<int:pk>/delete/', TamerContractDelete.as_view(), name='tamer-contract-delete'),

    path('opportunity_contract/create/', TamerOpportunityContactCreate.as_view(), name='tamer-opportunity-contact-create'),
    path('opportunity_contract/<int:pk>/update/', TamerOpportunityContactUpdate.as_view(), name='tamer-opportunity-contact-update'),
    path('opportunity_contract/<int:pk>/delete/', TamerOpportunityContactDelete.as_view(), name='tamer-opportunity-contact-delete'),

]
