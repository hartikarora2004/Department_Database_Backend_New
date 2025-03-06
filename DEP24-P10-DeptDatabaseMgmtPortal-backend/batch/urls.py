from django.urls import path
app_name = 'Batch'
from .views import *

urlpatterns = [
    path('',BatchList.as_view()),
    path('create/',BatchCreate.as_view()),
    path('<int:id>/',BatchDetailView.as_view()),
]