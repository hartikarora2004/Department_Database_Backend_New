from django.contrib import admin
from django.urls import path
app_name = 'event'
from .views import *

urlpatterns = [
    path('',EventList.as_view()),
    path('user/',EventUserList.as_view()),
    path('create/',EventCreate.as_view()),
    path('create/upload/',EventListUploadView.as_view()),
    path('<int:id>/',EventDetailView.as_view()),
    path('restore/<int:id>/',EventRestoreView.as_view()),
    path('draft/',EventDraftListView.as_view()),
    path('draft/<int:id>/',EventDraftView.as_view()),
    path('submit/<int:id>/',EventSubmitView.as_view()),
    path('approve/<int:id>/',EventApproveView.as_view()),
    path('reject/<int:id>/',EventRejectView.as_view()),
    path('pending/',EventPendingListView.as_view()),
    path('deleted/',EventDeletedListView.as_view()),
    path('definitions/',definations),
    path('record-edit', record_edit, name='record-edit'),
]