from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from task.models import Task

class TaskSerializer(ModelSerializer):
    snippet = serializers.ReadOnlyField(source='get_snippet')
    task_url = serializers.URLField(source='get_task_url', read_only=True)
    relative_url = serializers.URLField(source='get_absolute_url', read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name='get_abs_url')
    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'content','snippet', 'complete','task_url','relative_url','absolute_url', 'created_date', 'updated_date']
        read_only_fields = ['id' , 'user', 'created_date','updated_date', 'complete']

    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        return super().create(validated_data)
    
    def get_abs_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri()
