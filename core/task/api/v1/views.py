from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


from django.shortcuts import get_object_or_404
from task.models import Task
from .serializers import TaskSerializer
from .paginations import TaskPagination


class TaskViewSets(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TaskPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['complete']


    def get_queryset(self):
        user = self.request.user
        tasks = Task.objects.filter(user=user)
        return tasks
    
    @action(methods=['get'],detail=True)
    def get_done(self,request,pk=None):
        task = get_object_or_404(Task,pk=pk, user=request.user)
        task.complete = True
        task.save()
        serializer = TaskSerializer(instance=task)
        return Response({
            'Status': 'Done',
            'detail': serializer.data,
        })