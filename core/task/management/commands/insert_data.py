import random
from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User,Profile
from task.models import Task

class Command(BaseCommand):
    """
        this command when run by "python manage.py insert_data" create a user and user_profile
        and create 5 task with fake and random data 
    """
    help='inserting fake data'

    def __init__(self,*args, **kwargs):
        super(Command,self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        # create user instance & get it's profile
        user = User.objects.create_user(email=self.fake.email(), password='123456@mir')
        user_profile = Profile.objects.get(user=user)
        # update user profile with given data
        user_profile.first_name = self.fake.first_name()
        user_profile.last_name = self.fake.last_name()
        user_profile.description = self.fake.paragraph(nb_sentences=2)
        # save user profile
        user_profile.save()
        # create post samples
        # we can set number of posts
        number_of_tasks = 5
        for _ in range(number_of_tasks):
            Task.objects.create(
                user = user,
                title = self.fake.paragraph(nb_sentences=1),
                content = self.fake.paragraph(nb_sentences=5),
                complete = random.choice([True,False]),
                # set random status for complete of task
            )
        
        