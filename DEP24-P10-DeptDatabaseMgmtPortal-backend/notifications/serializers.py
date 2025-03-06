from rest_framework import serializers
from .models import baseNotification,userNotifications,broadcastNotifications

class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = userNotifications
        fields = ['id','created_at','redirect_link','message','notification']
        order_by = ['-created_at']


class BroadcastNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = broadcastNotifications
        fields = ['id','created_at','redirect_link','message','notification', 'department']
        order_by = ['-created_at']