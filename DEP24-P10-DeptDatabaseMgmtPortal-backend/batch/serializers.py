from rest_framework import serializers
from .models import Batch
from department.serializers import DepartmentSerializer

class BatchSerializer(serializers.ModelSerializer):
    Department = serializers.SerializerMethodField(read_only = True)

    def get_Department(self, obj):
        return [DepartmentSerializer(obj.department).data]

    model = Batch
    class Meta:
        model = Batch
        fields = ['id',
                  'name',
                  'year',
                  'department',
                  'Department'
                  ]
        extra_kwargs = {
            'department': {'write_only': True, 'required': True},
        }