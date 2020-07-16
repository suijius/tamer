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

from tamer_app_contact.views import TamerContactView, TamerContactCreate, TamerContactDetail, TamerContactUpdate, TamerContactDelete, \
    TamerKindContactView, TamerKindContactCreate, TamerKindContactDetail, TamerKindContactUpdate, TamerKindContactDelete, \
    TamerContactNoteCreate, TamerContactNoteDetail, TamerContactNoteUpdate, TamerContactNoteDelete

urlpatterns = [
    path('contact/', TamerContactView.as_view(), name='tamer-contact-view'),
    path('contact/create/', TamerContactCreate.as_view(), name='tamer-contact-create'),
    path('contact/<int:pk>/', TamerContactDetail.as_view(), name='tamer-contact-detail'),
    path('contact/<int:pk>/update/', TamerContactUpdate.as_view(), name='tamer-contact-update'),
    path('contact/<int:pk>/delete/', TamerContactDelete.as_view(), name='tamer-contact-delete'),

    path('contact_note/create/', TamerContactNoteCreate.as_view(), name='tamer-contact-note-create'),
    path('contact_note/<int:pk>/', TamerContactNoteDetail.as_view(), name='tamer-contact-note-detail'),
    path('contact_note/<int:pk>/update/', TamerContactNoteUpdate.as_view(), name='tamer-contact-note-update'),
    path('contact_note/<int:pk>/delete/', TamerContactNoteDelete.as_view(), name='tamer-contact-note-delete'),

    path('kind_contact/', TamerKindContactView.as_view(), name='tamer-kind-contact-view'),
    path('kind_contact/create/', TamerKindContactCreate.as_view(), name='tamer-kind-contact-create'),
    path('kind_contact/<int:pk>/', TamerKindContactDetail.as_view(), name='tamer-kind-contact-detail'),
    path('kind_contact/<int:pk>/update/', TamerKindContactUpdate.as_view(), name='tamer-kind-contact-update'),
    path('kind_contact/<int:pk>/delete/', TamerKindContactDelete.as_view(), name='tamer-kind-contact-delete'),
]
