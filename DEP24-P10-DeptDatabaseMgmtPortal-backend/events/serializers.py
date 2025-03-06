from rest_framework import serializers
from .models import Event, EventEditHistory
from basemodel.serializers import *
from usercustom.serializers import *
from department.serializers import *

Event_fields = [
                  'title',
                  'description',
                  'link',
                  'type',
                  'date',
                  'venue',
                  'organizers',
                  'Organizers',
                  'speakers',
                  'number_of_participants'
                ]

Event_kwargs = {
            'organizers': {'write_only': True, 'required': True}
        }

class EventSerializer(BaseSerializer):
    Organizers = UserSerializer(many=True,read_only=True, source='organizers.all')
    model = Event

    def get_users_str(self):
        return ",".join([str(user) for user in self.validated_data['organizers']])

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
        for user in self.validated_data['organizers']:
            arr[dict_map[user.user_type]] = True
        print(arr)
        for i in range(4):
            if arr[i]:
                output += tags[i] + ','
        return output[:-1]

    class Meta:
        model = Event
        fields =  model_basic_fields + Event_fields
        extra_kwargs = {**model_base_kwargs , **Event_kwargs}



class EventDraftSerializer(BaseDraftSerializer):
    Organizers = UserSerializer(many=True,read_only=True, source='organizers.all')
    model = Event

    def get_users_str(self):
        return ",".join([str(user) for user in self.validated_data['organizers']])

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
        for user in self.validated_data['organizers']:
            arr[dict_map[user.user_type]] = True
        print(arr)
        for i in range(4):
            if arr[i]:
                output += tags[i] + ','
        return output[:-1]
    class Meta:
        model = Event
        fields =  model_basic_fields + Event_fields
        extra_kwargs = {**model_base_kwargs , **Event_kwargs}



class EventDraftUpdateSerializer(BaseDraftUpdateSerializer):
    Organizers = UserSerializer(many=True,read_only=True, source='organizers.all')
    model = Event

    def get_users_str(self):
        return ",".join([str(user) for user in self.validated_data['organizers']])

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
        for user in self.validated_data['organizers']:
            arr[dict_map[user.user_type]] = True
        print(arr)
        for i in range(4):
            if arr[i]:
                output += tags[i] + ','
        return output[:-1]
    class Meta:
        model = Event
        fields =  model_basic_fields + Event_fields
        extra_kwargs = {**model_base_kwargs , **Event_kwargs}

Event_list_fields = [
                  'id',
                  'title',
                  'description',
                  'link',
                  'type',
                  'date',
                  'venue',
                  'organizers',
                  'speakers',
                  'users',
                  'department',
                  'number_of_participants',
                  'created_by',
                    'tags'
                ]

class EventListSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.first_name', read_only=True)

    class Meta:
        model = Event
        fields = Event_list_fields

class EventEditHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventEditHistory
        fields = '__all__'