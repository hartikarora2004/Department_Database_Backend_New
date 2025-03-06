from .models import StudentProject
from .serializers import StudentProjectSerializer
from rest_framework import generics
from .services import *
from .access import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from basemodel.views import *
from rest_framework.decorators import api_view
from django_filters import rest_framework as filte
from django.db.models import Q


class StudentProjFilter(filte.FilterSet):
    title = filte.CharFilter(lookup_expr='icontains')
    user = filte.NumberFilter(field_name='members__id')
    from_date = filte.DateFilter(field_name='date', method = 'filter_from_date')
    to_date = filte.DateFilter(field_name='date', method = 'filter_to_date')
    tags = filte.CharFilter(field_name='tags', lookup_expr='icontains')
    department=filte.CharFilter(field_name='departments_code')
    class Meta:
        model = StudentProject
        fields = ['title','user', 'from_date', 'to_date', 'tags','department']

    def filter_to_date(self, queryset, name, value):
        return queryset.filter(
            Q(date__lte=value) | Q(date__isnull=True)
        )

    def filter_from_date(self, queryset, name, value):
        return queryset.filter(
            Q(date__gte=value) | Q(date__isnull=True)
        )



class StudentProjectList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = StudentProjectServices().get_list()
    serializer_class = StudentProjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = StudentProjFilter
    search_fields = ['$title','$description']

class StudentProjectUserList(baseModelUserList):
    access = StudentProjectAccessSpecifier()
    service = StudentProjectServices()
    model = StudentProject

class StudentProjectCreate(baseModelCreate):
    access = StudentProjectAccessSpecifier()
    service = StudentProjectServices()
    model = StudentProject

class StudentProjectDetailView(baseModelDetailView):
    access = StudentProjectAccessSpecifier()
    service = StudentProjectServices()
    model = StudentProject

class StudentProjectRestoreView(baseModelRestoreView):
    access = StudentProjectAccessSpecifier()
    service = StudentProjectServices()
    model = StudentProject

class StudentProjectDraftListView(baseModelDraftListView):
    access = StudentProjectAccessSpecifier()
    service = StudentProjectDraftServices()
    model = StudentProject

class StudentProjectDraftView(baseModelDraftView):
    access = StudentProjectAccessSpecifier()
    service = StudentProjectDraftServices()
    model = StudentProject

class StudentProjectSubmitView(baseModelSubmitView):
    access = StudentProjectAccessSpecifier()
    service = StudentProjectDraftServices()
    model = StudentProject

class StudentProjectApproveView(baseModelApproveView):
    access = StudentProjectAccessSpecifier()
    service = StudentProjectDraftServices()
    model = StudentProject

class StudentProjectRejectView(baseModelRejectView):
    access = StudentProjectAccessSpecifier()
    service = StudentProjectDraftServices()
    model = StudentProject

class StudentProjectPendingListView(baseModelPendingListView):
    access = StudentProjectAccessSpecifier()
    service = StudentProjectDraftServices()
    model = StudentProject

class StudentProjectDeletedListView(baseModelDeletedListView):
    access = StudentProjectAccessSpecifier()
    service = StudentProjectServices()
    model = StudentProject

@api_view(['GET'])
def definations(request):
    object_types = dict(StudentProject.object_status.choices)
    StudentProject_status = dict(StudentProject.StudentProjectStatus.choices)

    return Response({'definations':{'object_type':object_types,'status':StudentProject_status}},status = status.HTTP_200_OK)

class StudentProjectListUploadView(BaseListUploadView):
    access = StudentProjectAccessSpecifier()
    service = StudentProjectServices()
    model = StudentProject
    serializer = StudentProjectSerializer
    req = None
    filename = 'static/download_files/studentproj.xlsm'
    return_filename = 'studentproj.xlsm'

    def add_validators(self,ws):
        ws = super().add_validators(ws)
        for i in range(1000):
            rule = openpyxl.worksheet.datavalidation.DataValidation(type="list", formula1 = 'sheet3!$A2:$A99999', allow_blank=True)
            rule.error = 'Please select a valid option'
            rule.errorTitle = 'Invalid option'
            ws.add_data_validation(rule)
            rule.add(f'C{i+3}')