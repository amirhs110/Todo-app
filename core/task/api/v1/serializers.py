from rest_framework.serializers import ModelSerializer
from task.models import Task

class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'content', 'complete', 'created_date', 'updated_date']
        read_only_fields = ['id' , 'user', 'created_date','updated_date', 'complete']

    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        return super().create(validated_data)