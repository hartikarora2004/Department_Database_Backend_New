from django.contrib import admin
from .models import baseNotification,userNotifications,broadcastNotifications
# Register your models here.

admin.site.register(userNotifications)
admin.site.register(broadcastNotifications)