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

from tamer_app_employee.views import TamerEmployeeView, TamerEmployeeCreate, TamerEmployeeDetail, TamerEmployeeUpdate, TamerEmployeeDelete, \
    TamerPositionView, TamerPositionCreate, TamerPositionDetail, TamerPositionUpdate, TamerPositionDelete#, \
    # TamerContactNoteCreate, TamerContactNoteDetail, TamerContactNoteUpdate, TamerContactNoteDelete

urlpatterns = [
    path('employee/', TamerEmployeeView.as_view(), name='tamer-employee-view'),
    path('employee/create/', TamerEmployeeCreate.as_view(), name='tamer-employee-create'),
    path('employee/<int:pk>/', TamerEmployeeDetail.as_view(), name='tamer-employee-detail'),
    path('employee/<int:pk>/update/', TamerEmployeeUpdate.as_view(), name='tamer-employee-update'),
    path('employee/<int:pk>/delete/', TamerEmployeeDelete.as_view(), name='tamer-employee-delete'),
    #
    # path('contact_note/create/', TamerContactNoteCreate.as_view(), name='tamer-contact-note-create'),
    # path('contact_note/<int:pk>/', TamerContactNoteDetail.as_view(), name='tamer-contact-note-detail'),
    # path('contact_note/<int:pk>/update/', TamerContactNoteUpdate.as_view(), name='tamer-contact-note-update'),
    # path('contact_note/<int:pk>/delete/', TamerContactNoteDelete.as_view(), name='tamer-contact-note-delete'),
    #
    path('position/', TamerPositionView.as_view(), name='tamer-position-view'),
    path('position/create/', TamerPositionCreate.as_view(), name='tamer-position-create'),
    path('position/<int:pk>/', TamerPositionDetail.as_view(), name='tamer-position-detail'),
    path('position/<int:pk>/update/', TamerPositionUpdate.as_view(), name='tamer-position-update'),
    path('position/<int:pk>/delete/', TamerPositionDelete.as_view(), name='tamer-position-delete'),
]
