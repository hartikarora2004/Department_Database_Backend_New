from .models import Achievement
from .serializers import AchievementSerializer,AchievementListSerializer,AchievementEditHistorySerializer
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
from logger_config import logger
from usercustom.models import CustomUser as User
class AchievementFilter(filte.FilterSet):
    """
    Filter for Achievement
    Filter by filed and value
    title: matches with partial value of title
    user: search for participant with id
    from_date: search for date greater than or equal to from_date
    to_date: search for date less than or equal to to_date
    tags: search for tags given tags(regex)
    department: search for department with code
    """
    title = filte.CharFilter(lookup_expr='icontains')
    user = filte.NumberFilter(field_name='participants__id')
    from_date = filte.DateFilter(field_name='date', method = 'filter_from_date')
    to_date = filte.DateFilter(field_name='date', method = 'filter_to_date')
    tags = filte.CharFilter(field_name='tags', lookup_expr='regex')
    department=filte.NumberFilter(field_name='department__id')
    class Meta:
        model = Achievement
        fields = ['title', 'from_date', 'to_date', 'tags','user','department']
    
    def filter_from_date(self, queryset, name, value):
        return queryset.filter(
            Q(date__gte=value) | Q(date__isnull=True)
        )
    
    def filter_to_date(self, queryset, name, value):
        return queryset.filter(
            Q(date__lte=value) | Q(date__isnull=True)
        )

class AchievementList(generics.ListAPIView):
    """
    List of all achievements
    method: GET
    Filter by: title, user, from_date, to_date, tags, department
    search by: title, tags
    order by: date, title, participants
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = AchievementServices().get_list()
    serializer_class = AchievementListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = AchievementFilter
    search_fields = ['$title','$tags']
    ordering_fields = ['date','title','participants__id']

class AchievementUserList(baseModelUserList):
    access = AchievementAccessSpecifier()
    service = AchievementServices()
    model = Achievement

class AchievementCreate(baseModelCreate):
    access = AchievementAccessSpecifier()
    service = AchievementServices()

    model = Achievement

class AchievementDetailView(baseModelDetailView):
    access = AchievementAccessSpecifier()
    service = AchievementServices()
    model = Achievement

class AchievementRestoreView(baseModelRestoreView):
    access = AchievementAccessSpecifier()
    service = AchievementServices()
    model = Achievement

class AchievementDraftListView(baseModelDraftListView):
    access = AchievementAccessSpecifier()
    service = AchievementDraftServices()
    model = Achievement

class AchievementDraftView(baseModelDraftView):
    access = AchievementAccessSpecifier()
    service = AchievementDraftServices()
    model = Achievement

class AchievementSubmitView(baseModelSubmitView):
    access = AchievementAccessSpecifier()

    service = AchievementDraftServices()
    model = Achievement
    # first prints the baseModelSubmitView then typeo
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Type: Achievement")
        logger.info("Type: Achievement")

class AchievementApproveView(baseModelApproveView):
    access = AchievementAccessSpecifier()
    service = AchievementDraftServices()
    model = Achievement

class AchievementRejectView(baseModelRejectView):
    access = AchievementAccessSpecifier()
    service = AchievementDraftServices()
    model = Achievement

class AchievementPendingListView(baseModelPendingListView):
    access = AchievementAccessSpecifier()
    service = AchievementDraftServices()
    model = Achievement

class AchievementDeletedListView(baseModelDeletedListView):
    access = AchievementAccessSpecifier()
    service = AchievementServices()
    model = Achievement

@api_view(['GET'])
def definations(request):
    object_types = dict(Achievement.object_status.choices)
    Achievement_types = dict(Achievement.AchievementType.choices)
    
    return Response({'definations':{'object_type':object_types,'type':Achievement_types}},status = status.HTTP_200_OK)


class AchievementsListUploadView(BaseListUploadView):
    access = AchievementAccessSpecifier()
    service = AchievementServices()
    model = Achievement
    serializer = AchievementSerializer
    req = None
    filename = "static/download_files/achievements.xlsm"
    return_filename = "achievements.xlsm"

@api_view(['POST'])
def record_edit(request):
    serializer = AchievementEditHistorySerializer(data=request.data)
    print("valid")
    if serializer.is_valid():
        serializer.save()
        print("Achievement: " + f"{serializer.data['achievement']}" + " edited by user: "+str(request.user.id))
        logger.info("Achievement Record edited by user: "+str(request.user.id))
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
