from .models import Publication, PublicationEditHistory
from .serializers import PublicationListSerializer,PublicationEditHistorySerializer
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
from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

class PublicationFilter(filte.FilterSet):
    title = filte.CharFilter(lookup_expr='icontains')
    user = filte.NumberFilter(field_name='authors__id')
    authors_text = filte.CharFilter(lookup_expr='icontains')
    # allow null values for date fields
    from_date_published = filte.DateFilter(field_name='published_date', method='filter_from_date_published')
    to_date_published = filte.DateFilter(field_name='published_date', method='filter_to_date_published')
    from_date_accepted = filte.DateFilter(field_name='accepted_date', method='filter_from_date_accepted')
    to_date_accepted = filte.DateFilter(field_name='accepted_date', method='filter_to_date_accepted')
    tags = filte.CharFilter(field_name='tags', lookup_expr='icontains')
    department=filte.NumberFilter(field_name='department__id')
    class Meta:
        model = Publication
        fields = ['title','user', 'from_date_published', 'to_date_published','from_date_accepted', 'to_date_accepted','tags', 'authors_text','publication_type','publication_status','department']

    def filter_to_date_accepted(self, queryset, name, value):
        return queryset.filter(
            Q(accepted_date__lte=value) | Q(accepted_date__isnull=True)
        )
    
    def filter_from_date_accepted(self, queryset, name, value):
        return queryset.filter(
            Q(accepted_date__gte=value) | Q(accepted_date__isnull=True)
        )
    
    def filter_to_date_published(self, queryset, name, value):
        return queryset.filter(
            Q(published_date__lte=value) | Q(published_date__isnull=True)
        )
    
    def filter_from_date_published(self, queryset, name, value):
        return queryset.filter(
            Q(published_date__gte=value) | Q(published_date__isnull=True)
        )

class PublicationList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PublicationServices().get_list()
    serializer_class = PublicationListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = PublicationFilter
    search_fields = ['$title','$identifier']

class PublicationUserList(baseModelUserList):
    access = PublicationAccessSpecifier()
    service = PublicationServices()
    model = Publication

class PublicationCreate(baseModelCreate):
    access = PublicationAccessSpecifier()
    service = PublicationServices()
    model = Publication

class PublicationDetailView(baseModelDetailView):
    access = PublicationAccessSpecifier()
    service = PublicationServices()
    model = Publication

class PublicationRestoreView(baseModelRestoreView):
    access = PublicationAccessSpecifier()
    service = PublicationServices()
    model = Publication

class PublicationDraftListView(baseModelDraftListView):
    access = PublicationAccessSpecifier()
    service = PublicationDraftServices()
    model = Publication

class PublicationDraftView(baseModelDraftView):
    access = PublicationAccessSpecifier()
    service = PublicationDraftServices()
    model = Publication

class PublicationSubmitView(baseModelSubmitView):
    access = PublicationAccessSpecifier()
    service = PublicationDraftServices()
    model = Publication
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Type: Publications")
        logger.info("Type: Publications")


class PublicationApproveView(baseModelApproveView):
    access = PublicationAccessSpecifier()
    service = PublicationDraftServices()
    model = Publication

class PublicationRejectView(baseModelRejectView):
    access = PublicationAccessSpecifier()
    service = PublicationDraftServices()
    model = Publication

class PublicationPendingListView(baseModelPendingListView):
    access = PublicationAccessSpecifier()
    service = PublicationDraftServices()
    model = Publication

class PublicationDeletedListView(baseModelDeletedListView):
    access = PublicationAccessSpecifier()
    service = PublicationServices()
    model = Publication

@api_view(['GET'])
def definations(request):
    object_types = dict(Publication.object_status.choices)
    publication_types = dict(Publication.PublicationType.choices)
    publication_status = dict(Publication.PublicationStatus.choices)
    identifier_types = dict(Publication.IdentifierType.choices)
    field_tags_dict = dict(Publication.FieldTags.choices)
    return Response({'definations':{'object_type':object_types,'publication_type':publication_types,'publication_status':publication_status,'identifier_type':identifier_types, 'field_tags':field_tags_dict}},status = status.HTTP_200_OK)



class PublicationListUploadView(BaseListUploadView):
    access = PublicationAccessSpecifier()
    service = PublicationServices()
    model = Publication
    serializer = PublicationSerializer
    req = None
    filename = 'static/download_files/publications.xlsm'
    return_filename = 'publications.xlsm'

    def add_validators(self,ws):
        ws = super().add_validators(ws)
        for i in range(1000):
            rule = openpyxl.worksheet.datavalidation.DataValidation(type="list", formula1 = 'sheet5!$A2:$A99999', allow_blank=True)
            rule.error = 'Please select a valid option'
            rule.errorTitle = 'Invalid option'
            ws.add_data_validation(rule)
            rule.add(f'K{i+3}')
        for i in range(1000):
            rule = openpyxl.worksheet.datavalidation.DataValidation(type="list", formula1 = 'sheet6!$A2:$A99999', allow_blank=True)
            rule.error = 'Please select a valid option'
            rule.errorTitle = 'Invalid option'
            ws.add_data_validation(rule)
            rule.add(f'L{i+3}')
        for i in range(1000):
            rule = openpyxl.worksheet.datavalidation.DataValidation(type="list", formula1 = 'sheet7!$A2:$A99999', allow_blank=True)
            rule.error = 'Please select a valid option'
            rule.errorTitle = 'Invalid option'
            ws.add_data_validation(rule)
            rule.add(f'M{i+3}')

@api_view(['POST'])
def record_edit(request):
    print("request",request.data)
    serializer = PublicationEditHistorySerializer(data=request.data)
    if serializer.is_valid():
        print("Publications: " + f"{serializer.data['publication']}" + " edited by user: "+str(request.user.id))
        logger.info("Publications: " + f"{serializer.data['publication']}" + " edited by user: "+str(request.user.id))

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class PublicationEditHistoryListView(APIView):
#     def get(self, request, pk):
#         try:
#             publication = Publication.objects.get(pk=pk)
#             edits = PublicationEditHistory.objects.filter(publication=publication).order_by('-edited_at')[:3]
#             serializer = PublicationEditHistorySerializer(edits, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Publication.DoesNotExist:
#             return Response({"error": "Publication not found"}, status=status.HTTP_404_NOT_FOUND)