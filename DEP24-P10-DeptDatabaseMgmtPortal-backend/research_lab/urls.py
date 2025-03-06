from django.urls import path
app_name = 'research_labs'
from .views import *

urlpatterns = [
    path('',ResearchLabList.as_view()),
    path('user/',ResearchLabUserList.as_view()),
    path('create/',ResearchLabCreate.as_view()),
    path('<int:id>/',ResearchLabDetailView.as_view()),
    path('restore/<int:id>/',ResearchLabRestoreView.as_view()),
    path('deleted/',ResearchLabDeletedListView.as_view()),
    path('definitions/',definations),
]