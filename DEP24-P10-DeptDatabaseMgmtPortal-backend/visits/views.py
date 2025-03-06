from .models import Visit
from .serializers import VisitListSerializer
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

class VisitFilter(filte.FilterSet):
    title = filte.CharFilter(lookup_expr='icontains')
    user = filte.NumberFilter(field_name='user__id')
    from_date = filte.DateFilter(field_name='date', method = 'filter_from_date')
    to_date = filte.DateFilter(field_name='date', method = 'filter_to_date')
    tags = filte.CharFilter(field_name='tags', lookup_expr='icontains')
    department=filte.NumberFilter(field_name='department__id')
    class Meta:
        model = Visit
        fields = ['title', 'from_date', 'to_date','user', 'tags','department']

    def filter_to_date(self, queryset, name, value):
        return queryset.filter(
            Q(date__lte=value) | Q(date__isnull=True)
        )

    def filter_from_date(self, queryset, name, value):
        return queryset.filter(
            Q(date__gte=value) | Q(date__isnull=True)
        )


class VisitList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = VisitServices().get_list()
    serializer_class = VisitListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = VisitFilter
    search_fields = ['$title']

class VisitUserList(baseModelUserList):
    access = VisitAccessSpecifier()
    service = VisitServices()
    model = Visit

class VisitCreate(baseModelCreate):
    access = VisitAccessSpecifier()
    service = VisitServices()
    model = Visit

class VisitDetailView(baseModelDetailView):
    access = VisitAccessSpecifier()
    service = VisitServices()
    model = Visit

class VisitRestoreView(baseModelRestoreView):
    access = VisitAccessSpecifier()
    service = VisitServices()
    model = Visit

class VisitDraftListView(baseModelDraftListView):
    access = VisitAccessSpecifier()
    service = VisitDraftServices()
    model = Visit

class VisitDraftView(baseModelDraftView):
    access = VisitAccessSpecifier()
    service = VisitDraftServices()
    model = Visit

class VisitSubmitView(baseModelSubmitView):
    access = VisitAccessSpecifier()
    service = VisitDraftServices()
    model = Visit
    print("Type: Visits")
    logger.info("Type: Visits")

class VisitApproveView(baseModelApproveView):
    access = VisitAccessSpecifier()
    service = VisitDraftServices()
    model = Visit

class VisitRejectView(baseModelRejectView):
    access = VisitAccessSpecifier()
    service = VisitDraftServices()
    model = Visit

class VisitPendingListView(baseModelPendingListView):
    access = VisitAccessSpecifier()
    service = VisitDraftServices()
    model = Visit

class VisitDeletedListView(baseModelDeletedListView):
    access = VisitAccessSpecifier()
    service = VisitServices()
    model = Visit

@api_view(['GET'])
def definations(request):
    object_types = dict(Visit.object_status.choices)
    Visit_types = dict(Visit.VisitType.choices)

    return Response({'definations':{'object_type':object_types,'type':Visit_types}},status = status.HTTP_200_OK)


class VisitListUploadView(BaseListUploadView):
    access = VisitAccessSpecifier()
    service = VisitServices()
    model = Visit
    serializer = VisitSerializer
    req = None
    filename = "static/download_files/visits.xlsm"
    return_filename = "visits.xlsm"

    # def preprocess(self, data):
    #     data = super().preprocess(data)
    #     if self.req.user.id == data['user']:
    #         return data
    #     elif data['user'] == None:
    #         data['user'] = self.req.user.id
    #         return data
    #     else:
    #         raise Exception('Current user must be user of visit')

@api_view(['POST'])
def record_edit(request):
    serializer = VisitEditHistorySerializer(data=request.data)
    if serializer.is_valid():
        print("valid")
        serializer.save()
        print("Visits: " + f"{serializer.data['visits']}" + " edited by user: "+str(request.user.id))
        logger.info("Visits Record edited by user: "+str(request.user.id))
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)