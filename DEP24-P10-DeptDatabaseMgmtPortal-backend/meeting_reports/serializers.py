from .models import DinfoMeetingFile, BogMeetingFile
from rest_framework import serializers

class DinfoMeetingFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DinfoMeetingFile
        fields = '__all__'


class BogMeetingFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BogMeetingFile
        fields = '__all__'