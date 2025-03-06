from django.contrib import admin
from django.urls import path
app_name = 'project'
from .views import *

urlpatterns = [
    path('',ProjectList.as_view()),
    path('user/',ProjectUserList.as_view()),
    path('create/',ProjectCreate.as_view()),
    path('create/upload/',ProjectListUploadView.as_view()),
    path('<int:id>/',ProjectDetailView.as_view()),
    path('restore/<int:id>/',ProjectRestoreView.as_view()),
    path('draft/',ProjectDraftListView.as_view()),
    path('draft/<int:id>/',ProjectDraftView.as_view()),
    path('submit/<int:id>/',ProjectSubmitView.as_view()),
    path('approve/<int:id>/',ProjectApproveView.as_view()),
    path('reject/<int:id>/',ProjectRejectView.as_view()),
    path('pending/',ProjectPendingListView.as_view()),
    path('deleted/',ProjectDeletedListView.as_view()),
    path('definitions/',definations),
    path('record-edit', record_edit, name='record-edit'),
]


