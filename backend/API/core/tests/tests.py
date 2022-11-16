from django.test import TestCase


from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APISimpleTestCase, APITransactionTestCase
from rest_framework.test import APIRequestFactory


from core.models import User, Project, UserManager
from core.tests.factories import UserFactory, ProjectFactory
from core.views import RegistrationView, LoginView, LogoutView, ChangePasswordView, UserList, UserDetail, ProjectList, ProjectDetail
import random





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
        


# User creation tests
class test_case_user_registration(APITestCase):
    
    
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