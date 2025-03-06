from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ApproveRequest
from .serializers import ApprovalRequestSerializer

class ApproveRequestCreateView(APIView):
    def post(self, request):
        data = request.data
        instructor_id = data.get('instructor_id')
        achievement_id = data.get('achievement_id')

        approval_request = ApproveRequest.objects.create(
            applicant_name=data.get('applicant_name'),
            instructor_id=instructor_id,
            achievement_id=achievement_id
        )

        serializer = ApprovalRequestSerializer(approval_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
