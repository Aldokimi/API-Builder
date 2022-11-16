import json
from django.test import TestCase

<<<<<<< HEAD
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, CoreAPIClient, APITransactionTestCase, RequestsClient, APIClient
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
=======

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APISimpleTestCase, APITransactionTestCase
from rest_framework.test import APIRequestFactory

>>>>>>> 1af2fe3 (SWC-47: Added registration test case, modified settings MIDDLEWARE section order)

from core.models import User, Project, UserManager
from core.tests.factories import UserFactory, ProjectFactory
from core.views import RegistrationView, LoginView, LogoutView, ChangePasswordView, UserList, UserDetail, ProjectList, ProjectDetail
import random


<<<<<<< HEAD
from django.core.management import call_command


# # The Test class only tests those methods who name begins with a lower-case test.... 
# # So you can put in extra helper methods TestA and TestB which won't get run unless you explicitly call them.


# def make_db ():
#     '''Dynamically creates a database''' 
       
#     people = []
#     for _ in range(10):
#         person = UserFactory()
#         people.append(person)
        
#     for _ in range(50):
#         owner = random.choice(people)
#         project = ProjectFactory(owner=owner)
=======



# The Test class only tests those methods who name begins with a lower-case test.... 
# So you can put in extra helper methods TestA and TestB which won't get run unless you explicitly call them.


def make_db ():
    '''Dynamically creates a database''' 
       
    people = []
    for _ in range(10):
        person = UserFactory()
        people.append(person)
        
    for _ in range(50):
        owner = random.choice(people)
        project = ProjectFactory(owner=owner)
        

>>>>>>> 1af2fe3 (SWC-47: Added registration test case, modified settings MIDDLEWARE section order)

# User creation tests
class test_case_user_registration(APITestCase):
    
<<<<<<< HEAD
    def setUp(self):
        '''Set up the initial stuff before running the test cases'''
        self.url = 'http://127.0.0.1:8000/api/register/'

        # Load the database and fill the database
        call_command("seed", verbosity=0)

        self.valid_payload = {
            "username": "test_user_creation",
            "email": "test_user_creation@email.com",
            "password": "passwordXD",
            "password2": "passwordXD",
            "date_of_birth": "2000-10-22T00:00:00Z",
        }

        # all_users = User.objects.all()
        random_user = User.objects.order_by('?')[0]

        # Test data
        self.existing_user_payload = {
            "username": random_user.username,
            "email": random_user.email,
            "password": "passwordXD",
            "password2": "passwordXD",
            "date_of_birth": "2000-10-22T00:00:00Z"
        }

        self.invalid_email_payload = {
            "username": "test_user_creation",
            "email": "test_user_creation.email.com",
            "password": "passwordXD",
            "password2": "passwordXD",
            "date_of_birth": "2000-10-22T00:00:00Z"
        }

        self.invalid_password_payload = {
            "username": "test_user_creation",
            "email": "test_user_creation.email.com",
            "password": "passwordXD",
            "password2": "passwow",
            "date_of_birth": "2000-10-22T00:00:00Z"
        }

    def preform_test(self, data):
        factory = APIRequestFactory()
        request = factory.post(self.url, data, format='json')
        user_view = RegistrationView.as_view()
        response = user_view(request)
        return response
    
    def test_register_new_user (self):
        '''Case to check if a new user creation is possible'''
    
        #User email does not exist
        response = self.preform_test(self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
         
         
    def test_register_existing_user(self):
        '''Case to check if user creation is possible where the email already exists'''
        
        #User email exists
        response = self.preform_test(self.existing_user_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_register_user_with_invalid_email(self):
        '''Case to check if user creation is possible where the username is email'''
        
        #User email exists
        response = self.preform_test(self.invalid_email_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_with_invalid_password(self):
        '''Case to check if user creation is possible where the password is invalid'''
        
        #User email exists
        response = self.preform_test(self.invalid_password_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)




class test_case_user_login(APITestCase):
    
    def setUp(self):
        '''Set up the initial stuff before running the test cases'''
        self.url = 'http://127.0.0.1:8000/api/login/'

        # Create a new user
        new_user_data = {
            "username": "test_user",
            "email": "test_user@email.com",
            "password": "password",
            "password2": "password",
            "date_of_birth": "2000-10-22T00:00:00Z",
        }

        factory = APIRequestFactory()
        request = factory.post('http://127.0.0.1:8000/api/register/', new_user_data, format='json')
        user_view = RegistrationView.as_view()
        response = user_view(request)

        if response.status_code == status.HTTP_201_CREATED:
            self.user = User.objects.filter(email="test_user@email.com").first()
        else:
            raise Exception("Error occurred during creating a test user!")

        # Test data
        self.valid_payload = {
            "email": self.user.email,
            "password": "password",
        }

        self.invalid_email_payload = {
            "email": "test_user_creation.email.com",
            "password": "defaultpassword",
        }

        self.none_existing_user_payload = {
            "email": "okay_this_is_a_random_user@email.com",
            "password": "defaultpassword",
        }

        self.invalid_password_payload = {
            "email": self.user.email,
            "password": "passwordXD",
        }

    def preform_test(self, data, user=None):
        request_factory = APIRequestFactory()

        # Class based view that you want to test
        view = LoginView.as_view()

        # Request object
        request = request_factory.post(
            path=self.url,
            data=data, 
            content_type="application/json"
        )

        # Response obtained from request returned from view
        response = view(request)
        return response
    
    def test_login_user (self):
        '''Case to check if a new user login is possible'''
    
        #User email does not exist
        response = self.preform_test(self.valid_payload, user=self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
         
    def test_login_none_existing_user(self):
        '''Case to check if user login is possible where the email already exists'''
        
        #User email exists
        response = self.preform_test(self.none_existing_user_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_login_user_with_invalid_email(self):
        '''Case to check if user login is possible where the username is email'''
        
        #User email exists
        response = self.preform_test(self.invalid_email_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_with_invalid_password(self):
        '''Case to check if user login is possible where the password is invalid'''
        
        #User email exists
        response = self.preform_test(self.invalid_password_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
=======
    
    def registerUser_new (self):
        '''Case to check if a new user creation is possible'''

        theUser = {
        "username": "test_user_creation",
        "email": "test_user_creation@email.com",
        "password": "passwordXD",
        "password2": "passwordXD",
        "date_of_birth": "2000-10-22T00:00:00Z"
        }
    
        #User email does not exist
        factory = APIRequestFactory()
        request = factory.post("/api/register/",theUser, format='json')
        user_view = RegistrationView.as_view()
        response = user_view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
         
         
    def registerUser_exist(self):
        '''Case to check if user creation is possible where the email already exists'''
        
        theUser = {
        "username": "test_user_creation",
        "email": "test_user_creation@email.com",
        "password": "passwordXD",
        "password2": "passwordXD",
        "date_of_birth": "2000-10-22T00:00:00Z"
        }
        
        all_users = User.objects.all()
        random_user = all_users[random.randint(0, len(all_users)-1)]
        theUser['email'] = random_user.email
        theUser['username'] = "test_user_creation_existing"
    
        #User email exists
        factory = APIRequestFactory()
        request = factory.post("/api/register/",theUser, format='json')
        user_view = RegistrationView.as_view()
        response = user_view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_user_registration(self):
        '''Dynamically combining both test cases to to allow sharing their own database'''
        
        make_db()
        self.registerUser_new()
        self.registerUser_exist()
        


# User login tests
class test_case_user_login(APITestCase):
   
   
    def loginUser_Exist_correctDetails(self):
        '''Case to check if correct credentials allow login '''
        
        print("WorkINPROGRESS")
        #This returns an error if the correct details are given: SWC-59
    
    
    def loginUser_Exist_incorrectDetails(self):
        '''Case to check if incorrect credentials allow login'''
        
        all_users = User.objects.all()
        random_user = all_users[random.randint(0, len(all_users)-1)]
        the_input = {
            "email": "dummyuser@dumdum.com",
            "password": "thiswontwork"
        }
        
        factory = APIRequestFactory()
        factory
        request = factory.post("/api/login/",the_input, format='json')
        user_view = LoginView.as_view()
        response = user_view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def loginUser_noExist(self):
        '''Case to check if nonexistent credentials allow login'''
        print('WorkINPROGRESS2')
       
       
    def test_user_login(self):
        '''Dynamically combining the test cases to allow sharing their own database'''
        
        #make_db()
        User.objects.create_user(email='dummyuser@dumdum.com',date_of_birth='2000-10-22T00:00:00Z',password='strongpassword')
        self.loginUser_Exist_correctDetails()
        self.loginUser_Exist_incorrectDetails()
        self.loginUser_noExist()
>>>>>>> 1af2fe3 (SWC-47: Added registration test case, modified settings MIDDLEWARE section order)
