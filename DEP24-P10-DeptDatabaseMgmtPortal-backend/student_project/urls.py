from django.contrib import admin
from django.urls import path
app_name = 'student_project'
from .views import *

urlpatterns = [
    path('',StudentProjectList.as_view()),
    path('user/',StudentProjectUserList.as_view()),
    path('create/',StudentProjectCreate.as_view()),
    path('create/upload/',StudentProjectListUploadView.as_view()),
    path('<int:id>/',StudentProjectDetailView.as_view()),
    path('restore/<int:id>/',StudentProjectRestoreView.as_view()),
    path('draft/',StudentProjectDraftListView.as_view()),
    path('draft/<int:id>/',StudentProjectDraftView.as_view()),
    path('submit/<int:id>/',StudentProjectSubmitView.as_view()),
    path('approve/<int:id>/',StudentProjectApproveView.as_view()),
    path('reject/<int:id>/',StudentProjectRejectView.as_view()),
    path('pending/',StudentProjectPendingListView.as_view()),
    path('deleted/',StudentProjectDeletedListView.as_view()),
    path('definitions/',definations),
]


