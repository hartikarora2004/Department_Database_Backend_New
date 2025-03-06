from django.contrib import admin
from django.urls import path
app_name = 'publication'
from .views import *

urlpatterns = [
    path('',PublicationList.as_view()),
    path('user/',PublicationUserList.as_view()),
    path('create/',PublicationCreate.as_view()),
    path('create/upload/',PublicationListUploadView.as_view()),
    path('<int:id>/',PublicationDetailView.as_view()),
    path('restore/<int:id>/',PublicationRestoreView.as_view()),
    path('draft/',PublicationDraftListView.as_view()),
    path('draft/<int:id>/',PublicationDraftView.as_view()),
    path('submit/<int:id>/',PublicationSubmitView.as_view()),
    path('approve/<int:id>/',PublicationApproveView.as_view()),
    path('reject/<int:id>/',PublicationRejectView.as_view()),
    path('pending/',PublicationPendingListView.as_view()),
    path('deleted/',PublicationDeletedListView.as_view()),
    path('definations/',definations),
    path('record-edit', record_edit, name='record-edit'),
]