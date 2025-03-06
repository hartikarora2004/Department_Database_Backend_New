from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
import io
from django.db import transaction
from django.contrib.auth.models import Group
from .models import QueryModel
from .serializers import QuerySerializer
from django.core.mail import EmailMessage,send_mail
from django.contrib.sites.shortcuts import get_current_site
from basemodel.htmlgenerator import json_to_html
from django.http import QueryDict
from usercustom.models import CustomUser

developer_emails = ['2020csb1121@iitrpr.ac.in', '2020csb1142@iitrpr.ac.in', '2020csb1129@iitrpr.ac.in', '2020csb1131@iitrpr.ac.in']
developer_emails += ['2021csb1129@iitrpr.ac.in']

class createView(generics.CreateAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = QuerySerializer

    def post(self, request, *args, **kwargs):

        temp = {}
        temp['user'] = request.user.id
        try:
            temp['screenshot'] = request.data['screenshot']
        except:
            pass
        temp['issue'] = request.data['issue']
        temp['issue_category'] = request.data['issue_category']
        # temp = request.data
        try:
            # qm = QueryModel.objects.create(**temp)
            # qm.save()
            # ser = QuerySerializer(qm)
            ser = QuerySerializer(data = temp)
            if not ser.is_valid():
                raise Exception(ser.errors)
            ser.save()
            print(ser.data)
            temp = ser.data
            try:
                current_site = get_current_site(request).domain
                url_to_file = current_site + ser.data['screenshot']
            except Exception as e:
                print(e)
                url_to_file = None
            temp['screenshot'] = url_to_file
            message = EmailMessage("New Query",json_to_html(temp),'donotreplydepartmentdata@gmail.com',developer_emails)
            message.content_subtype = "html"
            message.send(fail_silently = False)
            return Response({"data":temp,"errors":None}, status= status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"data":None, "errors":str(e)}, status = status.HTTP_400_BAD_REQUEST)
        # serializer = QuerySerializer(data=temp)
        # if serializer.is_valid():
        #     serializer.save()
        #     # get current url
        #     current_site = get_current_site(request).domain
        #     try:
        #         url_to_file = current_site + serializer.data['screenshot']
        #     except:
        #         url_to_file = None
        #     temp = serializer.data
        #     temp['screenshot'] = url_to_file 
        #     message = EmailMessage("New Query",json_to_html(temp),'donotreplydepartmentdata@gmail.com',developer_emails)
        #     message.content_subtype = "html"
        #     message.send(fail_silently = False)
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)