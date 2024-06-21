from django.contrib import admin
from .models import Task
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    model = Task
    list_display=('user', 'title', 'created_date', 'complete')
    list_filter=('user', 'complete')
    search_fields=('title', 'user')
    ordering=('-created_date',)

admin.site.register(Task,TaskAdmin)