from rest_framework import serializers
from .models import facultyDetails

class FacultyDetailsSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.username', read_only=True)

    class Meta:
        model = facultyDetails
        fields = '__all__'
