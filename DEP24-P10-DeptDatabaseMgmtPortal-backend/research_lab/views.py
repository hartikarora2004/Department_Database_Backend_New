from .models import ResearchLab
from .serializers import ResearchLabSerializer
from rest_framework import generics
from .services import *
from .access import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from basemodel.views import *
from rest_framework.decorators import api_view

class ResearchLabList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ResearchLabServices().get_list()
    serializer_class = ResearchLabSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['Head','name','code','description','id']
    search_fields = ['$name','$code']

class ResearchLabUserList(baseModelUserList):
    access = ResearchLabAccessSpecifier()
    service = ResearchLabServices()
    model = ResearchLab

class ResearchLabCreate(baseModelCreate):
    access = ResearchLabAccessSpecifier()
    service = ResearchLabServices()
    model = ResearchLab
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Type: ResearchLab")
        logger.info("Type: ResearchLab")

class ResearchLabDetailView(baseModelDetailView):
    access = ResearchLabAccessSpecifier()
    service = ResearchLabServices()
    model = ResearchLab

class ResearchLabRestoreView(baseModelRestoreView):
    access = ResearchLabAccessSpecifier()
    service = ResearchLabServices()
    model = ResearchLab

class ResearchLabDeletedListView(baseModelDeletedListView):
    access = ResearchLabAccessSpecifier()
    service = ResearchLabServices()
    model = ResearchLab

@api_view(['GET'])
def definations(request):
    object_types = dict(ResearchLab.object_status.choices)
    print("ResearchLab: " + f"{serializer.data['research_lab']}" + " edited by user: "+str(request.user.id))
    logger.info("ResearchLab: " + f"{serializer.data['research_lab']}" + " edited by user: "+str(request.user.id))
    return Response({'definations':{'object_type':object_types}},status = status.HTTP_200_OK)