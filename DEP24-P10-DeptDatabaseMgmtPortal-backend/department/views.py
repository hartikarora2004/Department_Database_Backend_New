from .models import Department
from .serializers import DepartmentSerializer
from rest_framework import generics
from rest_framework import status 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from logger_config import logger


class DepartmentList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['Hod','name','code','description','id']
    search_fields = ['$name','$code']

class DepartmentsList(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name','code','description']
    search_fields = ['$name','$code']


class DepartmentCreate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Staff').exists():
            ser = DepartmentSerializer(data=request.data)
            if ser.is_valid():
                ser.save()
                print("Department Created")
                logger.info("Department Created by " + str(request.user) + " with data " + str(request.data))
                return Response({"data":ser.data,"errors":None}, status=status.HTTP_200_OK)
            else:
                return Response({"data":None,"errors":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"data":None,'errors':'You are not authorized to create Department'},status=status.HTTP_401_UNAUTHORIZED)
        

class DepartmentDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            ser = DepartmentSerializer(Department.objects.get(id=id))
            return Response({"data":ser.data,"errors":None}, status=status.HTTP_200_OK)
        except Department.DoesNotExist:
            return Response({"data":None,"errors":"Department does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, id):
        obj = Department.objects.get(id=id)
        if request.user.groups.filter(name='Staff').exists() or request.user == obj.Hod:
            ser = DepartmentSerializer(obj,data=request.data)
            if ser.is_valid():
                ser.save()
                return Response({"data":ser.data,"errors":None}, status=status.HTTP_200_OK)
            else:
                return Response({"data":None,"errors":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"data":None,'errors':'You are not authorized to update Department'},status=status.HTTP_401_UNAUTHORIZED)
        
    def delete(self, request, id):
        obj = Department.objects.get(id=id)
        if request.user.groups.filter(name='Staff').exists():
            try:
                obj.delete()
                return Response({"data":None,"errors":None}, status=status.HTTP_200_OK)
            except:
                return Response({"data":None,"errors":"Department does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"data":None,'errors':'You are not authorized to delete Department'},status=status.HTTP_401_UNAUTHORIZED)
