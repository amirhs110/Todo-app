import os
from celery import Celery
from celery.schedules import crontab
from task.tasks import send_email_celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls send_email_celery() every 10 seconds.
    sender.add_periodic_task(10.0, send_email_celery.s(), name='send email every 10')

    # celery -A core beat