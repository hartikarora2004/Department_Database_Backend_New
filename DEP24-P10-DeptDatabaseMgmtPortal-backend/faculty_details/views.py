from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import facultyDetails
from .serializers import FacultyDetailsSerializer

@api_view(['GET'])
def faculty_list(request):
    faculties = facultyDetails.objects.all()
    serializer = FacultyDetailsSerializer(faculties, many=True)
    return Response(serializer.data)
