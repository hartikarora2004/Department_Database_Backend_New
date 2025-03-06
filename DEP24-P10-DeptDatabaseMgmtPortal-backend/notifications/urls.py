from django.contrib import admin
from django.urls import path
app_name = 'notifications/'
from .views import *

urlpatterns = [
    path('',BaseNotificationList.as_view()),
    path('viewed/',notificationViewed.as_view()),
    path('broadcast/',broadcast.as_view()),
]