from basemodel.serializers import BaseSerializer
from .models import ResearchLab
from rest_framework import serializers



class ResearchLabSerializer(BaseSerializer):
    HEAD = serializers.CharField(source='Head.username',read_only=True)
    model = ResearchLab

    def get_users_str(self):
        return f"{str(self.validated_data['Head'])}"

    class Meta:
        model = ResearchLab
        fields = ['id','name','code','description','website','Head','address',"HEAD",'lab_type','equipments','users']
        users = serializers.CharField(source='Head.username')
        extra_kwargs = {
            'Head': {'write_only': True, 'required': True},
        }
