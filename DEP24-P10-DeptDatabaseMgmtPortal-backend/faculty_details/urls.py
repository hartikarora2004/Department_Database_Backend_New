from django.urls import path
from .views import faculty_list

urlpatterns = [
    path('', faculty_list, name='faculty-list'),
]
