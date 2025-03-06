from django.urls import path
app_name = 'department'
from .views import *

urlpatterns = [
    path('',DepartmentList.as_view()),
    path('ls/', DepartmentsList.as_view()),
    path('create/',DepartmentCreate.as_view()),
    path('<int:id>/',DepartmentDetailView.as_view()),
]