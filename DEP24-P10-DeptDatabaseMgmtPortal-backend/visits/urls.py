from django.contrib import admin
from django.urls import path
app_name = 'Visit'
from .views import *

urlpatterns = [
    path('',VisitList.as_view()),
    path('user/',VisitUserList.as_view()),
    path('create/',VisitCreate.as_view()),
    path('create/upload/',VisitListUploadView.as_view()),
    path('<int:id>/',VisitDetailView.as_view()),
    path('restore/<int:id>/',VisitRestoreView.as_view()),
    path('draft/',VisitDraftListView.as_view()),
    path('draft/<int:id>/',VisitDraftView.as_view()),
    path('submit/<int:id>/',VisitSubmitView.as_view()),
    path('approve/<int:id>/',VisitApproveView.as_view()),
    path('reject/<int:id>/',VisitRejectView.as_view()),
    path('pending/',VisitPendingListView.as_view()),
    path('deleted/',VisitDeletedListView.as_view()),
    path('definitions/',definations),
    path('record-edit', record_edit, name='record-edit'),
]