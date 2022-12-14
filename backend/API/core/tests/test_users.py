from core.models import User
from core.views import RegistrationView, LoginView, ChangePasswordView, UserDetail

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from rest_framework.authtoken.models import Token
from django.contrib.sessions.middleware import SessionMiddleware

from django.core.management import call_command


class test_case_user_registration(APITestCase):
    
    
    @classmethod
    def setUpTestData(self):

        '''Set up the initial stuff before running the test cases'''
        self.url = 'http://127.0.0.1:8000/api/register/'

        # Load the database and fill the database
        call_command("seed", verbosity=0)

        self.valid_payload = {
            "username": "test_case_user_registration",
            "email": "test_case_user_registration@email.com",
            "password": "passwordXD",
            "password2": "passwordXD",
            "date_of_birth": "2000-10-22T00:00:00Z"
        }

        random_user = User.objects.order_by('?')[0]

        # Test data
        self.existing_user_payload = {
            "username": random_user.username,
            "email": random_user.email,
            "password": "defaultpassword",
            "password2": "defaultpassword",
            "date_of_birth": "2000-10-22T00:00:00Z"
        }
        
        self.invalid_email_payload = {
            "username": "test_case_user_registration_invalid",
            "email": "test_case_user_registration_invalid.email.com",
            "password": "passwordXD",
            "password2": "passwordXD",
            "date_of_birth": "2000-10-22T00:00:00Z"
        }

        self.invalid_password_payload = {
            "username": "test_case_user_registration",
            "email": "test_case_user_registration@email.com",
            "password": "passwordXD",
            "password2": "passwow",
            "date_of_birth": "2000-10-22T00:00:00Z"
        }


    def Perform_Test(self, data):
        
        factory = APIRequestFactory()
        request = factory.post(self.url, data, format='json')
        user_view = RegistrationView.as_view()
        response = user_view(request)
        return response
    
    
    def test_register_new_user (self):
        '''Case to check if a new user creation is possible'''
    
        #User email does not exist
        response = self.Perform_Test(self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
         
         
    def test_register_existing_user(self):
        '''Case to check if user creation is possible where the email already exists'''
        
        #User email exists
        response = self.Perform_Test(self.existing_user_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_register_user_with_invalid_email(self):
        '''Case to check if user creation is possible where the email is incorrect '''
        
        #User email invalid
        response = self.Perform_Test(self.invalid_email_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_register_user_with_invalid_password(self):
        '''Case to check if user creation is possible where the password is invalid'''
        
        #User password invalid
        response = self.Perform_Test(self.invalid_password_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class test_case_user_login(APITestCase):
    
    
    @classmethod
    def setUpTestData(self):
        '''Set up the initial stuff before running the test cases'''
        self.url = 'http://127.0.0.1:8000/api/login/'

        # Create a new user
        new_user_data = {
            "username": "test_case_user_login",
            "email": "test_case_user_login@email.com",
            "password": "password69",
            "password2": "password69",
            "date_of_birth": "2000-10-22T00:00:00Z"
        }

        factory = APIRequestFactory()
        request = factory.post('http://127.0.0.1:8000/api/register/', new_user_data, format='json')
        user_view = RegistrationView.as_view()
        response = user_view(request)

        if response.status_code == status.HTTP_201_CREATED:
            self.user = User.objects.filter(email="test_case_user_login@email.com").first()
            self.token = Token.objects.create(user=self.user)
            self.token.save()
        else:
            raise Exception("Error occurred during creating a test user!")


        # Test data
        self.valid_payload = {
            "email": self.user.email,
            "password": "password69"
        }

        self.invalid_email_payload = {
            "email": "test_user_creation.email.com",
            "password": "defaultpassword"
        }

        self.none_existing_user_payload = {
            "email": "idontexistemail@email.com",
            "password": "defaultpassword"
        }

        self.invalid_password_payload = {
            "email": self.user.email,
            "password": "passwordINVALID"
        }
        
        
    def Perform_Test(self, data, user=None):
        
        request_factory = APIRequestFactory()
        view = LoginView.as_view()

        request = request_factory.post(self.url, data, format="json", HTTP_AUTHORIZATION='Token {}'.format(self.token))
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        force_authenticate(request, user)

        # Response obtained from request returned from view
        response = view(request)
        return response
    
    
    def test_login_user (self):
        '''Case to check if a new user login is possible'''
    
        #User email exists
        response = self.Perform_Test(self.valid_payload, self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
         
         
    def test_login_none_existing_user(self):
        '''Case to check if user login is possible where the email already exists'''
        
        #User email does not exist
        response = self.Perform_Test(self.none_existing_user_payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_login_user_with_invalid_email(self):
        '''Case to check if user login is possible where the username is email'''
        
        #User email is incorrect
        response = self.Perform_Test(self.invalid_email_payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_login_user_with_invalid_password(self):
        '''Case to check if user login is possible where the password is invalid'''
        
        #User email exists but password is incorrect
        response = self.Perform_Test(self.invalid_password_payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



class test_case_user_delete(APITestCase):
    
    @classmethod
    def setUpTestData(self):
        
        u1 = {
            "username": "test1",
            "email": "test_user1@email.com",
            "password": "bruhLOGIN1",
            "password2": "bruhLOGIN1",
            "date_of_birth": "2000-10-22T00:00:00Z"
        }
        u2 = {
            "username": "test2",
            "email": "test_user2@email.com",
            "password": "bruhLOGIN2",
            "password2": "bruhLOGIN2",
            "date_of_birth": "2000-10-22T00:00:00Z"
        }

        
        factory = APIRequestFactory()
        request1 = factory.post('http://127.0.0.1:8000/api/register/', u1, format='json')
        request2 = factory.post('http://127.0.0.1:8000/api/register/', u2, format='json')
        user_view1 = RegistrationView.as_view()
        user_view2 = RegistrationView.as_view()
        response1 = user_view1(request1)
        response2 = user_view2(request2)

        if response1.status_code == status.HTTP_201_CREATED and response2.status_code == status.HTTP_201_CREATED:
            pass
        else:
            raise Exception("Error occurred during creating a test user!")
        
        
        self.user1_payload = {
            "email": "test_user1@email.com",
            "password": "bruhLOGIN1"
        }
        self.user2_payload = {
            "email": "test_user2@email.com",
            "password": "bruhLOGIN2"
        }
        self.user_invalid = {
            "email": "iam_invalid@email.com",
            "password": "iam_invalid"
        }
        
        
    def Perform_Test(self, user1, user2=None):
        
        #Logging into the user
        factory_login = APIRequestFactory()
        user_view_login = LoginView.as_view()
        
        request_login = factory_login.post('http://127.0.0.1:8000/api/login/',user1, format='json')
        middleware = SessionMiddleware()
        middleware.process_request(request_login)
        request_login.session.save()
        force_authenticate(request_login, user1)
        response_login = user_view_login(request_login)
    
        if not response_login.status_code == status.HTTP_200_OK:
            raise Exception("(test_case_user_delete-Perform_Test): Error occurred during login to test user!")    
        
        factory_official = APIRequestFactory()
        user_view_official = UserDetail.as_view()
        theURL = "http://127.0.0.1:8000/api/users/"
        
        #User1 wants to delete user2
        if(user2):
            
            x = User.objects.filter(email=user2['email']).first()
            request_official = factory_official.delete(f"{theURL}{x.id}", user2, format='json', HTTP_AUTHORIZATION=f"Bearer {response_login.data['access']}")
            response_official = user_view_official(request_official, pk=x.id)
        #User1 wants to delete themselves
        else:
    
            x = User.objects.filter(email=user1['email']).first()
            #request_official = factory_official.delete(f"{theURL}{x.id}", user1, format='json') #auth failure error code 401
            #request_official = factory_official.delete(f"{theURL}{x.id}", user1, format='json', HTTP_AUTHORIZATION=f"Bearer {get_tokens_for_user(x)['access']}") #works
            request_official = factory_official.delete(f"{theURL}{x.id}", user1, format='json',HTTP_AUTHORIZATION=f"Bearer {response_login.data['access']}")
            response_official = user_view_official(request_official, pk=x.id)
        return response_official
    
    
    def test_delete_user_owner(self):
        '''Case to check if the user can delete themselves'''
        
        response = self.Perform_Test(self.user1_payload)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        
    def test_delete_user_notowner(self):
        '''Case to check if a user can delete another user '''
        
        response = self.Perform_Test(self.user1_payload,self.user2_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        

class test_case_user_changepassword(APITestCase):
    
    @classmethod
    def setUpTestData(self):
        
        dumdumUser_changepassword = {
            "username": "dumdumUser_changepassword",
            "email": "dumdumUser_changepassword@email.com",
            "password": "bruhChangePassword",
            "password2": "bruhChangePassword",
            "date_of_birth": "2000-10-22T00:00:00Z"
        }
        
        self.user_payload_changePass = {
            "email": "dumdumUser_changepassword@email.com",
            "current_password": "bruhChangePassword",
            "new_password": "bruhChangePasswordNEW"
        }
        
        self.user_payload_toLoginNewPass = {
            "email":"dumdumUser_changepassword@email.com",
            "password":"bruhChangePasswordNEW"
        }
        self.user_payload_toLoginOldPass = {
            "email":"dumdumUser_changepassword@email.com",
            "password":"bruhChangePassword"
        }
        
        factory = APIRequestFactory()
        request = factory.post('http://127.0.0.1:8000/api/register/', dumdumUser_changepassword, format='json')
        user_view = RegistrationView.as_view()
        response = user_view(request)

        if response.status_code == status.HTTP_201_CREATED:
            pass
        else:
            raise Exception("Error occurred during creating a test user!")
        
    
    
    def Perform_Login(self,dataLogin):
        
        #Logging into the user
        factory_login = APIRequestFactory()
        user_view_login = LoginView.as_view()
        
        request_login = factory_login.post('http://127.0.0.1:8000/api/login/',dataLogin, format='json')
        middleware = SessionMiddleware()
        middleware.process_request(request_login)
        request_login.session.save()
        force_authenticate(request_login, dataLogin)
        response_login = user_view_login(request_login)
        
        
        if response_login.status_code == status.HTTP_200_OK:
            pass
        else:
            raise Exception("(test_case_user_changepassword-Perform_Login): Error occurred during login to test user!")
        
        return response_login
        
    def Perform_Test(self,dataLogin,dataPasswordChange):
      
        response_login = self.Perform_Login(dataLogin)
        
        factory_official = APIRequestFactory()
        user_view_official = ChangePasswordView.as_view()
        theURL = "http://127.0.0.1:8000/api/change-password/"
        
        
        request_official = factory_official.post(theURL, dataPasswordChange, format='json', HTTP_AUTHORIZATION=f"Bearer {response_login.data['access']}")
        response_official = user_view_official(request_official)

        return response_official
    
    
    def test_user_changepassword (self):
        '''Case to check if a logged in user can change their password, then logging into the new settings '''
        
        response_changepassword = self.Perform_Test(self.user_payload_toLoginOldPass,self.user_payload_changePass)
        self.assertEqual(response_changepassword.status_code, status.HTTP_204_NO_CONTENT)
        
        response_loginToNewPassword = self.Perform_Login(self.user_payload_toLoginNewPass)
        self.assertEqual(response_loginToNewPassword.status_code, status.HTTP_200_OK)
      