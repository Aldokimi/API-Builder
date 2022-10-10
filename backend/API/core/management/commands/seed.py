import random

from django.db import transaction
from django.core.management.base import BaseCommand

from ...models import User, Project
from ...tests.factories import UserFactory, ProjectFactory

NUM_OF_FAKE_USERS = 10
NUM_OF_FAKE_PROJECTS = 50

class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [User, Project]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")
        # Create all the users
        people = []
        for _ in range(NUM_OF_FAKE_USERS):
            person = UserFactory()
            people.append(person)

        # Add some users to clubs
        for _ in range(NUM_OF_FAKE_PROJECTS):
            owner = random.choice(people)
            project = ProjectFactory(owner=owner)
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded fake data into the database'))
