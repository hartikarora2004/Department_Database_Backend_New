from .models import Event
from .serializers import EventSerializer
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

class EventFilter(filte.FilterSet):
    title = filte.CharFilter(lookup_expr='icontains')
    user = filte.NumberFilter(field_name='organizers__id')
    speakers = filte.CharFilter(lookup_expr='icontains')
    from_date = filte.DateFilter(field_name='date', method = 'filter_from_date')
    to_date = filte.DateFilter(field_name='date', method = 'filter_to_date')
    tags = filte.CharFilter(field_name='tags', lookup_expr='icontains')
    department=filte.NumberFilter(field_name='department__id')
    class Meta:
        model = Event
        fields = ['title','speakers', 'from_date', 'to_date','user', 'tags','department']
    
    def filter_to_date(self, queryset, name, value):
        return queryset.filter(
            Q(date__lte=value) | Q(date__isnull=True)
        )

    def filter_from_date(self, queryset, name, value):
        return queryset.filter(
            Q(date__gte=value) | Q(date__isnull=True)
        )

class EventList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = EventServices().get_list()
    serializer_class = EventListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = EventFilter
    search_fields = ['$title','$organizers','$speakers']

class EventUserList(baseModelUserList):
    access = EventAccessSpecifier()
    service = EventServices()
    model = Event

class EventCreate(baseModelCreate):
    access = EventAccessSpecifier()
    service = EventServices()
    model = Event

class EventDetailView(baseModelDetailView):
    access = EventAccessSpecifier()
    service = EventServices()
    model = Event

class EventRestoreView(baseModelRestoreView):
    access = EventAccessSpecifier()
    service = EventServices()
    model = Event

class EventDraftListView(baseModelDraftListView):
    access = EventAccessSpecifier()
    service = EventDraftServices()
    model = Event

class EventDraftView(baseModelDraftView):
    access = EventAccessSpecifier()
    service = EventDraftServices()
    model = Event

class EventSubmitView(baseModelSubmitView):
    access = EventAccessSpecifier()
    service = EventDraftServices()
    model = Event
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Type: Event")
        logger.info("Type: Event")

class EventApproveView(baseModelApproveView):
    access = EventAccessSpecifier()
    service = EventDraftServices()
    model = Event

class EventRejectView(baseModelRejectView):
    access = EventAccessSpecifier()
    service = EventDraftServices()
    model = Event

class EventPendingListView(baseModelPendingListView):
    access = EventAccessSpecifier()
    service = EventDraftServices()
    model = Event

class EventDeletedListView(baseModelDeletedListView):
    access = EventAccessSpecifier()
    service = EventServices()
    model = Event

@api_view(['GET'])
def definations(request):
    object_types = dict(Event.object_status.choices)
    Event_types = dict(Event.EventType.choices)

    return Response({'definations':{'object_type':object_types,'type':Event_types}},status = status.HTTP_200_OK)


class EventListUploadView(BaseListUploadView):
    access = EventAccessSpecifier()
    service = EventServices()
    model = Event
    serializer = EventSerializer
    req = None
    filename = "static/download_files/events.xlsm"
    return_filename = "events.xlsm"

@api_view(['POST'])
def record_edit(request):
    serializer = EventEditHistorySerializer(data=request.data)
    if serializer.is_valid():
        print("valid")
        serializer.save()
        # print("Event: " + f"{serializer.data['event']}" + " edited by user: "+str(request.user.id))
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)