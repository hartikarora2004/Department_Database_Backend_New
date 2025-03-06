from .models import Batch
from .serializers import BatchSerializer
from rest_framework import generics
from rest_framework import status 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView
from logger_config import logger



class BatchList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name','year','department','id']


class BatchCreate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Staff').exists():
            ser = BatchSerializer(data=request.data)
            if ser.is_valid():
                ser.save()
                print("Batch Created")
                logger.info("Batch Created by " + str(request.user) + " with data " + str(request.data))
                return Response({"data":ser.data,"errors":None}, status=status.HTTP_200_OK)
            else:
                return Response({"data":None,"errors":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"data":None,'errors':'You are not authorized to create Batch'},status=status.HTTP_401_UNAUTHORIZED)
        

class BatchDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            ser = BatchSerializer(Batch.objects.get(id=id))
            return Response({"data":ser.data,"errors":None}, status=status.HTTP_200_OK)
        except Batch.DoesNotExist:
            return Response({"data":None,"errors":"Batch does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, id):
        obj = Batch.objects.get(id=id)
        if request.user.groups.filter(name='Staff').exists() or request.user == obj.Hod:
            ser = BatchSerializer(obj,data=request.data)
            if ser.is_valid():
                ser.save()
                return Response({"data":ser.data,"errors":None}, status=status.HTTP_200_OK)
            else:
                return Response({"data":None,"errors":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"data":None,'errors':'You are not authorized to update Batch'},status=status.HTTP_401_UNAUTHORIZED)
        
    def delete(self, request, id):
        obj = Batch.objects.get(id=id)
        if request.user.groups.filter(name='Staff').exists():
            try:
                obj.delete()
                return Response({"data":None,"errors":None}, status=status.HTTP_200_OK)
            except:
                return Response({"data":None,"errors":"Batch does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"data":None,'errors':'You are not authorized to delete Batch'},status=status.HTTP_401_UNAUTHORIZED)
