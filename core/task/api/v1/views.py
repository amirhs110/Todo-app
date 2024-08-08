from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


from django.shortcuts import get_object_or_404
from task.models import Task
from .serializers import TaskSerializer
from .paginations import TaskPagination


class TaskViewSets(ModelViewSet):
    queryset = Task.objects.all().order_by("-created_date")
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TaskPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["complete"]
    search_fields = ["title", "content"]
    ordering_fields = ["created_date"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            """
            when i run app and request to show swagger doc i see a type error:
            TypeError: Field 'id' expected a number but got <django.contrib.auth.models.AnonymousUser object at 0x7f9351027a90>.
            view's TaskViewSets raised exception during schema generation; use getattr(self, 'swagger_fake_view', False) to detect and short-circuit this

            The Type error is because drf_yasg is trying to generate the schema for your view and
            it's running into issues when it encounters *AnonymousUser objects*.
            The error message suggests that getattr(self, 'swagger_fake_view', False) can be used to detect and
            short-circuit this during schema generation.
            """
            # Return an empty queryset when generating schema
            return Task.objects.none()

        user = self.request.user
        tasks = Task.objects.filter(user=user).order_by("-created_date")
        return tasks

    @action(methods=["get"], detail=True)
    def get_done(self, request, pk=None):
        if getattr(self, "swagger_fake_view", False):
            # Return a placeholder response when generating schema
            return Response({"Status": "Done", "detail": {}})

        task = get_object_or_404(Task, pk=pk, user=request.user)
        if not task.complete:
            task.complete = True
            task.save()
            status = "Done"
        else:
            status = "Your task is already done."
        serializer = TaskSerializer(instance=task, context={"request": request})
        return Response(
            {
                "Status": status,
                "detail": serializer.data,
            }
        )
