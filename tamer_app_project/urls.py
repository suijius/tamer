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

from tamer_app_project.views import TamerProjectView, TamerProjectCreate, TamerProjectDetail, TamerProjectUpdate, \
    TamerProjectDelete, \
    TamerStageCreate, TamerStageDelete, TamerStageDetail, TamerStageUpdate, \
    TamerBusinessTripCreate, TamerBusinessTripDelete, TamerBusinessTripDetail, TamerBusinessTripUpdate, \
    TamerEducationCreate, TamerEducationDelete, TamerEducationDetail, TamerEducationUpdate, \
    TamerEquipmentCreate, TamerEquipmentDelete, TamerEquipmentDetail, TamerEquipmentUpdate, \
    TamerSubcontractCreate, TamerSubcontractDelete, TamerSubcontractDetail, TamerSubcontractUpdate

urlpatterns = [
    path('project/', TamerProjectView.as_view(), name='tamer-project-view'),
    path('project/create/', TamerProjectCreate.as_view(), name='tamer-project-create'),
    path('project/<int:pk>/', TamerProjectDetail.as_view(), name='tamer-project-detail'),
    path('project/<int:pk>/update/', TamerProjectUpdate.as_view(), name='tamer-project-update'),
    path('project/<int:pk>/delete/', TamerProjectDelete.as_view(), name='tamer-project-delete'),

    path('stage/create/', TamerStageCreate.as_view(), name='tamer-stage-create'),
    path('stage/<int:pk>/', TamerStageDetail.as_view(), name='tamer-stage-detail'),
    path('stage/<int:pk>/update/', TamerStageUpdate.as_view(), name='tamer-stage-update'),
    path('stage/<int:pk>/delete/', TamerStageDelete.as_view(), name='tamer-stage-delete'),

    path('subcontract/create/', TamerSubcontractCreate.as_view(), name='tamer-subcontract-create'),
    path('subcontract/<int:pk>/', TamerSubcontractDetail.as_view(), name='tamer-subcontract-detail'),
    path('subcontract/<int:pk>/update/', TamerSubcontractUpdate.as_view(), name='tamer-subcontract-update'),
    path('subcontract/<int:pk>/delete/', TamerSubcontractDelete.as_view(), name='tamer-subcontract-delete'),

    path('education/create/', TamerEducationCreate.as_view(), name='tamer-education-create'),
    path('education/<int:pk>/', TamerEducationDetail.as_view(), name='tamer-education-detail'),
    path('education/<int:pk>/update/', TamerEducationUpdate.as_view(), name='tamer-education-update'),
    path('education/<int:pk>/delete/', TamerEducationDelete.as_view(), name='tamer-education-delete'),

    path('equipment/create/', TamerEquipmentCreate.as_view(), name='tamer-equipment-create'),
    path('equipment/<int:pk>/', TamerEquipmentDetail.as_view(), name='tamer-equipment-detail'),
    path('equipment/<int:pk>/update/', TamerEquipmentUpdate.as_view(), name='tamer-equipment-update'),
    path('equipment/<int:pk>/delete/', TamerEquipmentDelete.as_view(), name='tamer-equipment-delete'),

    path('business_trip/create/', TamerBusinessTripCreate.as_view(), name='tamer-business-trip-create'),
    path('business_trip/<int:pk>/', TamerBusinessTripDetail.as_view(), name='tamer-business-trip-detail'),
    path('business_trip/<int:pk>/update/', TamerBusinessTripUpdate.as_view(), name='tamer-business-trip-update'),
    path('business_trip/<int:pk>/delete/', TamerBusinessTripDelete.as_view(), name='tamer-business-trip-delete'),

    path('section_charter/create/', TamerBusinessTripCreate.as_view(), name='tamer-section-charter-create'),
    path('section_charter/<int:pk>/', TamerBusinessTripDetail.as_view(), name='tamer-section-charter-detail'),
    path('section_charter/<int:pk>/update/', TamerBusinessTripUpdate.as_view(), name='tamer-section-charter-update'),
    path('section_charter/<int:pk>/delete/', TamerBusinessTripDelete.as_view(), name='tamer-section-charter-delete'),

    path('project_charter/create/', TamerBusinessTripCreate.as_view(), name='tamer-project-charter-create'),
    path('project_charter/<int:pk>/', TamerBusinessTripDetail.as_view(), name='tamer-project-charter-detail'),
    path('project_charter/<int:pk>/update/', TamerBusinessTripUpdate.as_view(), name='tamer-project-charter-update'),
    path('project_charter/<int:pk>/delete/', TamerBusinessTripDelete.as_view(), name='tamer-project-charter-delete'),
]
