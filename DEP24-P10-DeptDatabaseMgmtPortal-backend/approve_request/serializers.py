from rest_framework import serializers
from .models import ApproveRequest

class ApprovalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApproveRequest
        fields = ['id', 'applicant_name', 'instructor_id', 'achievement_id', 'request_date']
