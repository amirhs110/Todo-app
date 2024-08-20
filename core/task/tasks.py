from celery import shared_task
from time import sleep


@shared_task
def send_email_celery():
    sleep(5)
    print('yeeeeeeeees Done.')