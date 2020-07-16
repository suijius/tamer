from django.urls import path

from tamer_app_task.views import TamerTaskView, TamerTaskCreate, TamerTaskUpdate, TamerTaskDelete

urlpatterns = [
    path('task/', TamerTaskView.as_view(), name='tamer-task-view'),
    path('task/create/', TamerTaskCreate.as_view(), name='tamer-task-create'),
    path('task/<int:pk>/update/', TamerTaskUpdate.as_view(), name='tamer-task-update'),
    path('task/<int:pk>/delete/', TamerTaskDelete.as_view(), name='tamer-task-delete'),
]