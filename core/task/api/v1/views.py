from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from task.models import Task
from .serializers import TaskSerializer


class TaskViewSets(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        tasks = Task.objects.filter(user=user)
        return tasks