from rest_framework import serializers
from .models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    HOD = serializers.CharField(source='Hod.username',read_only=True)
    model = Department
    class Meta:
        model = Department
        fields = ['id',
                  'name',
                  'code',
                  'description',
                  'HOD',
                  'Hod'
                  ]
        extra_kwargs = {
            'Hod': {'write_only': True, 'required': True},
        }