from django.urls import path

from tamer_app_document.views import TamerDocumentTemplateView, TamerDocumentTemplateCreate, \
    TamerDocumentTemplateDetail, TamerDocumentTemplateUpdate, TamerDocumentTemplateDelete, \
    TamerDocumentTemplateSectionCreate, TamerDocumentTemplateSectionUpdate, \
    TamerDocumentTemplateSectionDelete, TamerDocumentView, TamerDocumentCreate, TamerDocumentDetail, \
    TamerDocumentUpdate, TamerDocumentDelete, TamerDocumentSectionCreate, TamerDocumentSectionUpdate, \
    TamerDocumentSectionDelete, TamerDocumentSectionApplyTemplate

urlpatterns = [
    path('document_template/', TamerDocumentTemplateView.as_view(), name='tamer-document-template-view'),
    path('document_template/create/', TamerDocumentTemplateCreate.as_view(), name='tamer-document-template-create'),
    path('document_template/<int:pk>/', TamerDocumentTemplateDetail.as_view(), name='tamer-document-template-detail'),
    path('document_template/<int:pk>/update/', TamerDocumentTemplateUpdate.as_view(),
         name='tamer-document-template-update'),
    path('document_template/<int:pk>/delete/', TamerDocumentTemplateDelete.as_view(),
         name='tamer-document-template-delete'),

    path('document_template_section/create/', TamerDocumentTemplateSectionCreate.as_view(),
         name='tamer-document-template-section-create'),
    path('document_template_section/<int:pk>/update/', TamerDocumentTemplateSectionUpdate.as_view(),
         name='tamer-document-template-section-update'),
    path('document_template_section/<int:pk>/delete/', TamerDocumentTemplateSectionDelete.as_view(),
         name='tamer-document-template-section-delete'),

    path('document/', TamerDocumentView.as_view(), name='tamer-document-view'),
    path('document/create/', TamerDocumentCreate.as_view(), name='tamer-document-create'),
    path('document/<int:pk>/', TamerDocumentDetail.as_view(), name='tamer-document-detail'),
    path('document/<int:pk>/update/', TamerDocumentUpdate.as_view(), name='tamer-document-update'),
    path('document/<int:pk>/delete/', TamerDocumentDelete.as_view(), name='tamer-document-delete'),

    path('document_section/create/', TamerDocumentSectionCreate.as_view(), name='tamer-document-section-create'),
    path('document_section/apply_template/', TamerDocumentSectionApplyTemplate.as_view(),
         name='tamer-document-section-apply-template'),
    path('document_section/<int:pk>/update/', TamerDocumentSectionUpdate.as_view(),
         name='tamer-document-section-update'),
    path('document_section/<int:pk>/delete/', TamerDocumentSectionDelete.as_view(),
         name='tamer-document-section-delete'),
    # path('kind_contact/', TamerKindContactView.as_view(), name='tamer-kind-contact-view'),
    # path('kind_contact/create/', TamerKindContactCreate.as_view(), name='tamer-kind-contact-create'),
    # path('kind_contact/<int:pk>/', TamerKindContactDetail.as_view(), name='tamer-kind-contact-detail'),
    # path('kind_contact/<int:pk>/update/', TamerKindContactUpdate.as_view(), name='tamer-kind-contact-update'),
    # path('kind_contact/<int:pk>/delete/', TamerKindContactDelete.as_view(), name='tamer-kind-contact-delete'),
]
