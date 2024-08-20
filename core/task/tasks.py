from celery import shared_task
from time import sleep
from django.apps import apps


@shared_task
def send_email_celery():
    sleep(5)
    print('yeeeeeeeees Done.')

@shared_task
def clear_completed_tasks():
    Task = apps.get_model('task', 'Task')
    completed_tasks = Task.objects.filter(complete=True)
    count = completed_tasks.delete()[0]
    # we get a tuple from delete function and get count of deleted posts from first item
    print(f"{count} completed tasks deleted for all users.")