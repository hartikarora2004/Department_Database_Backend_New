from rest_framework import serializers
from .models import Achievement, AchievementEditHistory
from basemodel.serializers import *
from usercustom.serializers import *

Achievement_fields = [
                  'title',
                  'description',
                  'link',
                  'type',
                  'date',
                  'participants',
                  'Participants',
                  'participants_text'
                ]

Achievement_kwargs = {
            'participants': {'write_only': True, 'required': True}
        }

class AchievementSerializer(BaseSerializer):
    Participants = UserSerializer(many=True,read_only=True, source='participants.all')
    model = Achievement

    def get_users_str(self):
        return ",".join([str(user) for user in self.validated_data['participants']])
    
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
        for user in self.validated_data['participants']:
            arr[dict_map[user.user_type]] = True
        print(arr)
        for i in range(4):
            if arr[i]:
                output += tags[i] + ','
        return output[:-1]

    class Meta:
        model = Achievement
        fields = model_basic_fields + Achievement_fields
        extra_kwargs = {**model_base_kwargs , **Achievement_kwargs}

class AchievementDraftSerializer(BaseDraftSerializer):
    Participants = UserSerializer(many=True,read_only=True, source='participants.all')
    model = Achievement

    def get_users_str(self):
        return ",".join([str(user) for user in self.validated_data['participants']])
    
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
        for user in self.validated_data['participants']:
            arr[dict_map[user.user_type]] = True
        print(arr)
        for i in range(4):
            if arr[i]:
                output += tags[i] + ','
        return output[:-1]
    
    class Meta:
        model = Achievement
        fields = model_basic_fields + Achievement_fields
        extra_kwargs = {**model_base_kwargs , **Achievement_kwargs}

class AchievementDraftUpdateSerializer(BaseDraftUpdateSerializer):
    Participants = UserSerializer(many=True,read_only=True, source='participants.all')
    model = Achievement

    def get_users_str(self):
        return ",".join([str(user) for user in self.validated_data['participants']])
    
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
        for user in self.validated_data['participants']:
            arr[dict_map[user.user_type]] = True
        print(arr)
        for i in range(4):
            if arr[i]:
                output += tags[i] + ','
        return output[:-1]
    class Meta:
        model = Achievement
        fields = model_basic_fields + Achievement_fields
        extra_kwargs = {**model_base_kwargs , **Achievement_kwargs}


Achievement_list_fields = [
                  'id',
                  'title',
                  'description',
                  'link',
                  'type',
                  'date',
                  'participants',
                  'participants_text',
                  'users',
                  'department',
                  'tags',
                  'created_by',
                ]

class AchievementListSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.first_name', read_only=True)
    class Meta:
        model = Achievement
        fields = Achievement_list_fields

class AchievementEditHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AchievementEditHistory
        fields = '__all__'