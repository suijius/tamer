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

from tamer_app_workflow.views import TamerWorkflowView, TamerWorkflowCreate, TamerWorkflowDetail, TamerWorkflowUpdate, \
    TamerWorkflowDelete, \
    TamerStateView, TamerStateCreate, TamerStateDetail, TamerStateUpdate, TamerStateDelete, TamerObjectCreate, \
    TamerObjectUpdate, TamerObjectDelete, \
    TamerActionCreate, TamerActionDelete, TamerActionUpdate, TamerStateEdgeDelete, TamerStateEdgeCreate, \
    TamerEdgeDelete, TamerEdgeUpdate, \
    TamerEdgeDetail, TamerEdgeCreate, TamerEdgeView, TamerActionEdgeCreate, TamerActionEdgeDelete, TamerActionEdgeUpdate

urlpatterns = [
    path('workflow/', TamerWorkflowView.as_view(), name='tamer-workflow-view'),
    path('workflow/create/', TamerWorkflowCreate.as_view(), name='tamer-workflow-create'),
    path('workflow/<int:pk>/', TamerWorkflowDetail.as_view(), name='tamer-workflow-detail'),
    path('workflow/<int:pk>/update/', TamerWorkflowUpdate.as_view(), name='tamer-workflow-update'),
    path('workflow/<int:pk>/delete/', TamerWorkflowDelete.as_view(), name='tamer-workflow-delete'),

    path('object/create/', TamerObjectCreate.as_view(), name='tamer-object-create'),
    path('object/<int:pk>/update/', TamerObjectUpdate.as_view(), name='tamer-object-update'),
    path('object/<int:pk>/delete/', TamerObjectDelete.as_view(), name='tamer-object-delete'),

    path('action/create/', TamerActionCreate.as_view(), name='tamer-action-create'),
    path('action/<int:pk>/update/', TamerActionUpdate.as_view(), name='tamer-action-update'),
    path('action/<int:pk>/delete/', TamerActionDelete.as_view(), name='tamer-action-delete'),

    # path('instance/', TamerWorkflowView.as_view(), name='tamer-instance-view'),
    # path('instance/create/', TamerWorkflowCreate.as_view(), name='tamer-instance-create'),
    # path('instance/<int:pk>/', TamerWorkflowDetail.as_view(), name='tamer-instance-detail'),
    # path('instance/<int:pk>/update/', TamerWorkflowUpdate.as_view(), name='tamer-instance-update'),
    # path('instance/<int:pk>/delete/', TamerWorkflowDelete.as_view(), name='tamer-instance-delete'),

    # path('action_edge/', TamerActionEdgeView.as_view(), name='tamer-action-edge-view'),
    path('action_edge/create/', TamerActionEdgeCreate.as_view(), name='tamer-action-edge-create'),
    # path('action_edge/<int:pk>/', TamerActionEdgeDetail.as_view(), name='tamer-action-edge-detail'),
    path('action_edge/<int:pk>/update/', TamerActionEdgeUpdate.as_view(), name='tamer-action-edge-update'),
    path('action_edge/<int:pk>/delete/', TamerActionEdgeDelete.as_view(), name='tamer-action-edge-delete'),

    path('state/', TamerStateView.as_view(), name='tamer-state-view'),
    path('state/create/', TamerStateCreate.as_view(), name='tamer-state-create'),
    path('state/<int:pk>/', TamerStateDetail.as_view(), name='tamer-state-detail'),
    path('state/<int:pk>/update/', TamerStateUpdate.as_view(), name='tamer-state-update'),
    path('state/<int:pk>/delete/', TamerStateDelete.as_view(), name='tamer-state-delete'),

    path('state_edge/create/', TamerStateEdgeCreate.as_view(), name='tamer-state-edge-create'),
    path('state_edge/<int:pk>/delete/', TamerStateEdgeDelete.as_view(), name='tamer-state-edge-delete'),

    path('edge/', TamerEdgeView.as_view(), name='tamer-edge-view'),
    path('edge/create/', TamerEdgeCreate.as_view(), name='tamer-edge-create'),
    path('edge/<int:pk>/', TamerEdgeDetail.as_view(), name='tamer-edge-detail'),
    path('edge/<int:pk>/update/', TamerEdgeUpdate.as_view(), name='tamer-edge-update'),
    path('edge/<int:pk>/delete/', TamerEdgeDelete.as_view(), name='tamer-edge-delete'),
]
