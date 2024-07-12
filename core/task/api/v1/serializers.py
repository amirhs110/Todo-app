from rest_framework.serializers import ModelSerializer
from task.models import Task

class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ['user', 'title', 'content', 'complete', 'created_date', 'updated_date']