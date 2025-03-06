from .models import Project
from .serializers import ProjectSerializer, ProjectDraftSerializer, ProjectEditHistorySerializer, ProjectListSerializer
from rest_framework import generics
from .services import *
from .access import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from basemodel.views import *
from rest_framework.decorators import api_view
from rest_framework.views import APIView
import json
from django_filters import rest_framework as filte
from django.db.models import Q

class ProjectFilter(filte.FilterSet):
    title = filte.CharFilter(lookup_expr='icontains')
    user = filte.NumberFilter(field_name='members__id')
    from_date = filte.DateFilter(field_name='start_date', method = 'filter_from_date')
    to_date = filte.DateFilter(field_name='start_date', method = 'filter_to_date')
    tags  = filte.CharFilter(field_name='tags', lookup_expr='icontains')
    status = filte.CharFilter(field_name='status', lookup_expr='exact')
    department=filte.NumberFilter(field_name='department__id')

    class Meta:
        model = Project
        fields = ['title','user','code','id','from_date','to_date','tags','status','department']
 
    def filter_to_date(self, queryset, name, value):
        return queryset.filter(
            Q(date__lte=value) | Q(date__isnull=True)
        )

    def filter_from_date(self, queryset, name, value):
        return queryset.filter(
            Q(date__gte=value) | Q(date__isnull=True)
        )

class ProjectList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ProjectServices().get_list()
    serializer_class = ProjectListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProjectFilter
    search_fields = ['$title','$description']

class ProjectUserList(baseModelUserList):
    access = ProjectAccessSpecifier()
    service = ProjectServices()
    model = Project

class ProjectCreate(baseModelCreate):
    access = ProjectAccessSpecifier()
    service = ProjectServices()
    model = Project
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Type: Project")
        logger.info("Type: Project")

class ProjectDetailView(baseModelDetailView):
    access = ProjectAccessSpecifier()
    service = ProjectServices()
    model = Project

class ProjectRestoreView(baseModelRestoreView):
    access = ProjectAccessSpecifier()
    service = ProjectServices()
    model = Project

class ProjectDraftListView(baseModelDraftListView):
    access = ProjectAccessSpecifier()
    service = ProjectDraftServices()
    model = Project

class ProjectDraftView(baseModelDraftView):
    access = ProjectAccessSpecifier()
    service = ProjectDraftServices()
    model = Project

class ProjectSubmitView(baseModelSubmitView):
    access = ProjectAccessSpecifier()
    service = ProjectDraftServices()
    model = Project
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Type: Project")
        logger.info("Type: Project")

class ProjectApproveView(baseModelApproveView):
    access = ProjectAccessSpecifier()
    service = ProjectDraftServices()
    model = Project

class ProjectRejectView(baseModelRejectView):
    access = ProjectAccessSpecifier()
    service = ProjectDraftServices()
    model = Project

class ProjectPendingListView(baseModelPendingListView):
    access = ProjectAccessSpecifier()
    service = ProjectDraftServices()
    model = Project

class ProjectDeletedListView(baseModelDeletedListView):
    access = ProjectAccessSpecifier()
    service = ProjectServices()
    model = Project

@api_view(['GET'])
def definations(request):
    object_types = dict(Project.object_status.choices)
    project_status = dict(Project.ProjectStatus.choices)

    return Response({'definations':{'object_type':object_types,'status':project_status}},status = status.HTTP_200_OK)


class ProjectListUploadView(BaseListUploadView):
    access = ProjectAccessSpecifier()
    service = ProjectServices()
    model = Project
    serializer = ProjectSerializer
    req = None
    filename = 'static/download_files/project.xlsm'
    return_filename = 'project.xlsm'

    def preprocess(self, data):
        data = super().preprocess(data)
        if self.req.user.id in data['members']:
            return data
        else:
            raise Exception('Current user must be a member of the project')
        
@api_view(['POST'])
def record_edit(request):
    serializer = ProjectEditHistorySerializer(data=request.data)
    if serializer.is_valid():
        print("valid") 
        serializer.save()
        print("Project: " + f"{serializer.data['project']}" + " edited by user: "+str(request.user.id))
        logger.info("Project: " + f"{serializer.data['project']}" + " edited by user: "+str(request.user.id))
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)