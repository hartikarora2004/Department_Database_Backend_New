from django.contrib import admin
from django.urls import path
app_name = 'achievement'
from .views import *

urlpatterns = [
    path('',AchievementList.as_view()),
    path('user/',AchievementUserList.as_view()),
    path('create/',AchievementCreate.as_view()),
    path('create/upload/',AchievementsListUploadView.as_view()),
    path('<int:id>/',AchievementDetailView.as_view()),
    path('restore/<int:id>/',AchievementRestoreView.as_view()),
    path('draft/',AchievementDraftListView.as_view()),
    path('draft/<int:id>/',AchievementDraftView.as_view()),
    path('submit/<int:id>/',AchievementSubmitView.as_view()),
    path('approve/<int:id>/',AchievementApproveView.as_view()),
    path('reject/<int:id>/',AchievementRejectView.as_view()),
    path('pending/',AchievementPendingListView.as_view()),
    path('deleted/',AchievementDeletedListView.as_view()),
    path('definitions/',definations),
    path('record-edit', record_edit, name='record-edit'),
]