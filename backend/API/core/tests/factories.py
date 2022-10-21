import factory
from factory.django import DjangoModelFactory
from ..models import User, Project

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    date_of_birth = factory.Faker('date_time')
    is_active = factory.Faker('pybool')
    is_admin = factory.Faker('pybool')
    linkedin_token = factory.Faker('uuid4')
    date_joined = factory.Faker('date_time')
    last_login  = factory.Faker('date_time')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    bio = factory.Faker('sentence')
    date_of_birth =factory.Faker('date_time')
    profile_picture = factory.Faker('image_url')
    password = factory.PostGenerationMethodCall('set_password','defaultpassword')

class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Faker('name')
    owner = factory.SubFactory(UserFactory)
    date_created = factory.Faker('date_time')
    last_updated = factory.Faker('date_time')
    endpoint_name= factory.Faker('uri')
    private = factory.Faker('pybool')
