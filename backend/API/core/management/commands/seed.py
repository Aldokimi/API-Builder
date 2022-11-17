import random

from django.db import transaction
from django.core.management.base import BaseCommand

from ...models import User, Project
from ...tests.factories import UserFactory, ProjectFactory
from ...utils import make_dir_for_project_of_user, make_dir_for_user, remove_dirs_of_user
 

NUM_OF_FAKE_USERS = 10
NUM_OF_FAKE_PROJECTS = 50

class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        
        self.stdout.write("Deleting old data...")
        models = [User, Project]
        tmpBoolForUsers = True
        
        for m in models:
            
            if(tmpBoolForUsers):
                for aUser in m.objects.all():
                    remove_dirs_of_user(str(aUser))
                tmpBoolForUsers = False
            m.objects.all().delete()

        self.stdout.write("Creating new data...")
        # Create all the users
        people = []
        for _ in range(NUM_OF_FAKE_USERS):
            person = UserFactory()
            people.append(person)
            make_dir_for_user(person.email)

        # Add some users to clubs
        for _ in range(NUM_OF_FAKE_PROJECTS):
            owner = random.choice(people)
            project = ProjectFactory(owner=owner)
            make_dir_for_project_of_user(owner.email, project.name)
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded fake data into the database'))
