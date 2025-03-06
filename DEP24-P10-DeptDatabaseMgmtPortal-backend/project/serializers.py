from rest_framework import serializers
from .models import Project, ProjectEditHistory
from basemodel.serializers import *
from usercustom.models import CustomUser
from usercustom.serializers import UserSerializer

Project_fields = [
                  'title',
                  'description',
                  'code',
                  'start_date',
                  'end_date',
                  'members',
                  'link',
                  'Members',
                  'investors',
                  'amount_invested',
                  'status'
                ]

Project_kwargs = {
            'members': {'write_only': True, 'required': True}
        }

class ProjectSerializer(BaseSerializer):
    Members = UserSerializer(many=True,read_only=True, source='members.all')
    model = Project

    def get_users_str(self):
        return ",".join([str(user) for user in self.validated_data['members']])
    
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
        for user in self.validated_data['members']:
            arr[dict_map[user.user_type]] = True
        print(arr)
        for i in range(4):
            if arr[i]:
                output += tags[i] + ','
        return output[:-1]

    class Meta:
        model = Project
        fields = model_basic_fields + Project_fields
        extra_kwargs = {**model_base_kwargs , **Project_kwargs}

    def validate(self, data):
        errors = {}
        for value in data['members']:
            if not value.is_activated:
                errors.setdefault('members', []).append("User is not activated")
            if not value.groups.filter(name='Faculty').exists():
                errors.setdefault('members', []).append(f"User {value.username} with id {value.id} is not a faculty")
        if errors:
            raise serializers.ValidationError(errors)
        return data


class ProjectDraftSerializer(BaseDraftSerializer):
    Members = UserSerializer(many=True,read_only=True, source='members.all')
    model = Project

    def get_users_str(self):
        return ",".join([str(user) for user in self.validated_data['members']])

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
        for user in self.validated_data['members']:
            arr[dict_map[user.user_type]] = True
        print(arr)
        for i in range(4):
            if arr[i]:
                output += tags[i] + ','
        return output[:-1]
    
    class Meta:
        model = Project
        fields = model_basic_fields + Project_fields
        extra_kwargs = {**model_base_kwargs , **Project_kwargs}

    def validate(self, data):
        errors = {}
        for value in data['members']:
            if not value.is_activated:
                errors.setdefault('members', []).append("User is not activated")
            if not value.groups.filter(name='Faculty').exists():
                errors.setdefault('members', []).append(f"User {value.username} with id {value.id} is not a faculty")
        if errors:
            raise serializers.ValidationError(errors)
        return data


class ProjectDraftUpdateSerializer(BaseDraftUpdateSerializer):
    Members = UserSerializer(many=True,read_only=True, source='members.all')
    model = Project

    def get_users_str(self):
        return ",".join([str(user) for user in self.validated_data['members']])

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
        for user in self.validated_data['members']:
            arr[dict_map[user.user_type]] = True
        print(arr)
        for i in range(4):
            if arr[i]:
                output += tags[i] + ','
        return output[:-1]
    
    class Meta:
        model = Project
        fields = model_basic_fields + Project_fields
        extra_kwargs = {**model_base_kwargs , **Project_kwargs}
    
    def validate(self, data):
        errors = {}
        for value in data['members']:
            if not value.is_activated:
                errors.setdefault('members', []).append("User is not activated")
            if not value.groups.filter(name='Faculty').exists():
                errors.setdefault('members', []).append(f"User {value.username} with id {value.id} is not a faculty")
        if errors:
            raise serializers.ValidationError(errors)
        return data
    

Project_list_fields = [
                  'id',
                  'users',
                  'department',
                  'title',
                  'description',
                  'code',
                  'start_date',
                  'end_date',
                  'members',
                  'link',
                  'investors',
                  'amount_invested',
                  'status',
                  'tags',
                  'created_by',
                ]

class ProjectListSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.first_name', read_only=True)
    class Meta:
        model = Project
        fields = Project_list_fields

class ProjectEditHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectEditHistory
        fields = '__all__'
