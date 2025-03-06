from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import userNotifications, broadcastNotifications
from .serializers import UserNotificationSerializer, BroadcastNotificationSerializer
from usercustom.models import CustomUser
from django.contrib.auth.models import Group
from .email_notification import email_notification,email_broadcast_notification


class BaseNotificationList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            user_notifications = userNotifications.objects.filter(user = request.user)
            user_serializer = UserNotificationSerializer(user_notifications,many=True)
            group_notifications_1 = broadcastNotifications.objects.filter(group__in = request.user.groups.all()).filter(department = request.user.department)
            group_notifications_2 = broadcastNotifications.objects.filter(group = None).filter(department = request.user.department)
            group_notifications = (group_notifications_1 |group_notifications_2).distinct()
            group_serializer = BroadcastNotificationSerializer(group_notifications,many=True)
            return Response({"data":{"user_notifications":user_serializer.data,"broadcast_notifications":group_serializer.data},"error":None},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)

class notificationViewed(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self,request):
        try:
            notification_id = request.data['notification_id']
            notification = userNotifications.objects.get(id = notification_id)
            print(notification.user,request.user)
            if(notification.user != request.user):
                return Response({"error":"Invalid request."},status=status.HTTP_400_BAD_REQUEST)
            ser = UserNotificationSerializer(notification)
            data = ser.data
            notification.delete()
            return Response({"error":None,'data': ser.data},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error":"Something went wrong",'data':None},status=status.HTTP_400_BAD_REQUEST)
    
    def post(self,request):
        try:
            ser = UserNotificationSerializer(data = request.data)
            if ser.is_valid():
                if(request.user.groups.filter(name = 'Staff').exists()):
                    if(request.data['user'] != None):
                        email_notification(request.data['notification'],request.data['message'] + '\n\n Redirect link: '+ request.data['redirect_link'],CustomUser.objects.get(id = request.data['user']))
                        ser.save(user = CustomUser.objects.get(id = request.data['user']))

                        return Response({"error":None,'data': ser.data},status=status.HTTP_200_OK)
                    else:
                        ser.save(user = request.user)
                        return Response({"error":None,'data': ser.data},status=status.HTTP_200_OK)
                else:
                    ser.save(user = request.user)
                    return Response({"error":None,'data': ser.data},status=status.HTTP_200_OK)
            else:
                return Response({"error":"Invalid data",'data':None},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error":"Something went wrong",'data':None},status=status.HTTP_400_BAD_REQUEST)
        
class broadcast(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self,request):
        if(request.user.groups.filter(name = 'Staff').exists() == False):
            return Response({"error":"Invalid request."},status=status.HTTP_400_BAD_REQUEST)
        try:
            broadcastNotifications.objects.get(id = request.data['notification_id']).delete()
            return Response({"error":None,'data': "deleted successfully"},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error":"Something went wrong",'data':None},status=status.HTTP_400_BAD_REQUEST)
        
    def post(self,request):
        if(request.user.groups.filter(name = 'Staff').exists() == False):
            return Response({"error":"Invalid request."},status=status.HTTP_400_BAD_REQUEST)
        try:
            temp_data = request.data.copy()
            temp_data['department'] = request.user.department.id
            ser = BroadcastNotificationSerializer(data = temp_data)
            if ser.is_valid():
                if 'group' not in request.data:
                    return Response({"errors":{"group":['Please select group.']},'data':None},status=status.HTTP_400_BAD_REQUEST)
                if request.data['group'] != 'All':
                    print('a')
                    ser.save(group = Group.objects.get(name = request.data['group']))
                    email_broadcast_notification(request, request.data['notification'],request.data['message'] + '\n\n Redirect link: ' + request.data['redirect_link'],Group.objects.get(name = request.data['group']))
                else:
                    print('b')
                    ser.save()
                    print('c')
                    email_broadcast_notification(request, request.data['notification'],request.data['message'] + '\n\n Redirect link: ' + request.data['redirect_link'],None)
                return Response({"error":None,'data': ser.data},status=status.HTTP_200_OK)
            else:
                return Response({"error":"Invalid data",'data':None},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error":"Something went wrong",'data':None},status=status.HTTP_400_BAD_REQUEST)