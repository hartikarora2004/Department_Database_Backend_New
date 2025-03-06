from rest_framework import serializers
from .models import Visit, VisitEditHistory
from basemodel.serializers import *
from usercustom.serializers import *
from department.serializers import *


Visit_fields = [
                  'title',
                  'user',
                  'User',
                  'from_date',
                  'to_date',
                  'venue',
                  'type',
                  'description',
                  'link'
            ]

Visit_kwargs = {
            'user': {'write_only': True, 'required': True}
        }

class VisitSerializer(BaseSerializer):
    # User =  UserSerializer(read_only=True, source='user')
    User =  serializers.SerializerMethodField()
    model = Visit

    def get_User(self, obj):
        return [UserSerializer(obj.user).data]

    def get_users_str(self):
        return f"{str(self.validated_data['user'])}"

    def generate_tags(self):
        arr = [False,False,False,False,False]
        tags = ['faculty', 'undergraduate', 'postgraduate', 'phd', 'staff']
        output = ''
        dict_map = {}
        dict_map['fc'] = 0
        dict_map['ug'] = 1
        dict_map['pg'] = 2
        dict_map['phd'] = 3
        dict_map['st'] = 4
        arr[dict_map[self.validated_data['user'].user_type]] = True
        for i in range(4):
            if arr[i]:
                output += tags[i] + ','
        return output[:-1]

    class Meta:
        model = Visit
        fields = model_basic_fields + Visit_fields
        extra_kwargs = {**model_base_kwargs , **Visit_kwargs} 

class VisitDraftSerializer(BaseDraftSerializer):
    User =  serializers.SerializerMethodField()
    model = Visit

    def get_User(self, obj):
        return [UserSerializer(obj.user).data]


    def get_users_str(self):
        return f"{str(self.validated_data['user'])}"

    def generate_tags(self):
        arr = [False,False,False,False,False]
        tags = ['faculty', 'undergraduate', 'postgraduate', 'phd', 'staff']
        output = ''
        dict_map = {}
        dict_map['fc'] = 0
        dict_map['ug'] = 1
        dict_map['pg'] = 2
        dict_map['phd'] = 3
        dict_map['st'] = 4
        arr[dict_map[self.validated_data['user'].user_type]] = True
        for i in range(4):
            if arr[i]:
                output += tags[i] + ','
        return output[:-1]
    
    class Meta:
        model = Visit
        fields = model_basic_fields + Visit_fields
        extra_kwargs = {**model_base_kwargs , **Visit_kwargs} 


class VisitDraftUpdateSerializer(BaseDraftUpdateSerializer):
    User =  serializers.SerializerMethodField()
    model = Visit

    def get_User(self, obj):
        return [UserSerializer(obj.user).data]


    
    def get_users_str(self):
        return f"{str(self.validated_data['user'])}"

    def generate_tags(self):
        arr = [False,False,False,False,False]
        tags = ['faculty', 'undergraduate', 'postgraduate', 'phd', 'staff']
        output = ''
        dict_map = {}
        dict_map['fc'] = 0
        dict_map['ug'] = 1
        dict_map['pg'] = 2
        dict_map['phd'] = 3
        dict_map['st'] = 4
        arr[dict_map[self.validated_data['user'].user_type]] = True
        for i in range(4):
            if arr[i]:
                output += tags[i] + ','
        return output[:-1]
    
    class Meta:
        model = Visit
        fields = model_basic_fields + Visit_fields
        extra_kwargs = {**model_base_kwargs , **Visit_kwargs}

Visit_list_fields = [
                  'id',
                  'users',
                  'department',
                  'title',
                  'user',
                  'from_date',
                  'to_date',
                  'venue',
                  'type',
                  'description',
                  'link',
                  'tags',
                  'created_by',
            ]

class VisitListSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.first_name', read_only=True)
    
    class Meta:
        model = Visit
        fields = Visit_list_fields

class VisitEditHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitEditHistory
        fields = '__all__'