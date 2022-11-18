from core.models import User, Project
from core.views import LoginView, ProjectList, ProjectDetail, ProjectHistoryDetail

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from rest_framework.authtoken.models import Token
from django.contrib.sessions.middleware import SessionMiddleware

from django.core.management import call_command

import random
import pygit2


# Official global login function to avoid code repetition
def globalPerformLogin(LoginPayload,className):
    '''Global function to login given user credentials, returns response'''
        
    #Logging into the user
    factory_login = APIRequestFactory()
    user_view_login = LoginView.as_view()
    
    request_login = factory_login.post('http://127.0.0.1:8000/api/login/',LoginPayload, format='json')
    middleware = SessionMiddleware()
    middleware.process_request(request_login)
    request_login.session.save()
    force_authenticate(request_login, LoginPayload)
    response_login = user_view_login(request_login)
    
    if not response_login.status_code == status.HTTP_200_OK:
        raise Exception(f"{className}: Error occurred during login to test user!")
    return response_login


class test_case_project_create(APITestCase):
    
    @classmethod
    def setUpTestData(self):
        
        call_command("seed", verbosity=0)
        
        random_user = User.objects.order_by('?')[0]
        self.dataLogin = {
            "email":f"{random_user.email}",
            "password":"defaultpassword"
        }
        
        self.valid_payload = {
            "name": "Some Project",
            "date_created": "1969-04-20T00:00:00Z",
            "last_updated": "2001-10-22T00:00:00Z",
            "owner": f"{random_user.id}"
        }
        
        self.invalid_payload = {
            "date_created": "1969-04-20T00:00:00Z",
            "last_updated": "2001-10-22T00:00:00Z"
        }
        
        self.another_owner_payload = {
            "name": "Some Project",
            "date_created": "1969-04-20T00:00:00Z",
            "last_updated": "2001-10-22T00:00:00Z",
            "owner": f"{1 if int(random_user.id) == 0 else (int(random_user.id) -1) }"
        }
        
        self.invalid_owner_payload = {
            "name": "Some Project",
            "date_created": "1969-04-20T00:00:00Z",
            "last_updated": "2001-10-22T00:00:00Z",
            "owner": "someSTUFF"
        }
        
        
    def Perform_Test(self,dataLogin,payload):
        
        response_login = globalPerformLogin(dataLogin,"test_case_project_create")
        
        factory_official = APIRequestFactory()
        user_view_official = ProjectList.as_view()
        theURL = "http://127.0.0.1:8000/api/projects/"
        
        request_official = factory_official.post(theURL, payload, format='json', HTTP_AUTHORIZATION=f"Bearer {response_login.data['access']}")
        response_official = user_view_official(request_official)

        return response_official
        
        
    def test_case_new_project(self):
        '''test case to check if a new project is created including its respective repo'''
        
        response = self.Perform_Test(self.dataLogin,self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        path = f"/home/API-Builder/{self.dataLogin['email']}/{self.valid_payload['name']}/"
        try:
            repo = pygit2.Repository(path)
            result = True
        except pygit2.GitError:
            result = False
        
        self.assertEqual(result,True)
            
    
    def test_case_invalid_project(self):
        
        response = self.Perform_Test(self.dataLogin,self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    
    def test_case_another_owner(self):
        
        response = self.Perform_Test(self.dataLogin,self.another_owner_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        

    def test_case_invalid_owner(self):
        
        response = self.Perform_Test(self.dataLogin,self.invalid_owner_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
               

class test_case_projects_view(APITestCase):
    
    @classmethod
    def setUpTestData(self):
        
        call_command("seed", verbosity=0)
        
        self.random_user = User.objects.order_by('?')[0]
        self.dataLogin = {
            "email":f"{self.random_user.email}",
            "password":"defaultpassword"
        }
        self.ProjectsTotal = len(Project.objects.all())
    
    
    def Perform_Test(self,loginPayload):
        
        response_login = globalPerformLogin(loginPayload,"test_case_projects_view")
        
        factory_official = APIRequestFactory()
        user_view_official = ProjectList.as_view()
        theURL = "http://127.0.0.1:8000/api/projects/"
        
        request_official = factory_official.get(theURL, loginPayload, format='json', HTTP_AUTHORIZATION=f"Bearer {response_login.data['access']}")
        response_official = user_view_official(request_official)

        return response_official
    
    
    def test_case_viewall_projects(self):
    
        response = self.Perform_Test(self.dataLogin)
        sameID = Project.objects.filter(owner=self.random_user.id)
        privates = Project.objects.filter(private=False)
        expectedTotal = len(sameID | privates)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),expectedTotal) 
     
        

class test_case_project_view(APITestCase):
    
    @classmethod
    def setUpTestData(self):
        
        call_command("seed", verbosity=0)
        
        self.random_user = User.objects.order_by('?')[0]
        self.login_payload = {
            "email":f"{self.random_user.email}",
            "password":"defaultpassword"
        }
        self.owned_projects = Project.objects.filter(owner=self.random_user.id)
        self.public_projects = Project.objects.filter(private=False)
        self.accessable_projects = self.owned_projects | self.public_projects
        self.inaccessable_projects = (Project.objects.all()).difference(self.accessable_projects)  
    
    
    def Perform_Test(self,loginPayload,prjID):
        
        response_login = globalPerformLogin(loginPayload,"test_case_project_view")
        
        factory_official = APIRequestFactory()
        user_view_official = ProjectDetail.as_view()
        theURL = f"http://127.0.0.1:8000/api/projects/{prjID}"
        
        request_official = factory_official.get(theURL, loginPayload, format='json', HTTP_AUTHORIZATION=f"Bearer {response_login.data['access']}")
        response_official = user_view_official(request_official,pk=prjID)

        return response_official
    
    
    def test_case_access_owned_prj(self):
        
        theID = (self.owned_projects.order_by('?')[0]).id
        response = self.Perform_Test(self.login_payload,theID)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    def test_case_access_public_prj(self):
        
        theID = (self.public_projects.order_by('?')[0]).id
        response = self.Perform_Test(self.login_payload,theID)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_case_access_viewable_projectlist(self):
        
        theID = (self.accessable_projects.order_by('?')[0]).id
        response = self.Perform_Test(self.login_payload,theID)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_case_access_unowned_prg(self):
        
        random_index = random.randint(1,len(self.inaccessable_projects)-1)
        theID = self.inaccessable_projects[random_index].id
        response = self.Perform_Test(self.login_payload,theID)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
      

class test_case_project_delete(APITestCase):
    
    @classmethod
    def setUpTestData(self):
        
        call_command("seed", verbosity=0)
        
        self.random_user = User.objects.order_by('?')[0]
        self.login_payload = {
            "email":f"{self.random_user.email}",
            "password":"defaultpassword"
        }
        self.owned_projects = Project.objects.filter(owner=self.random_user.id)
        self.public_projects = Project.objects.filter(private=False)
        self.accessable_projects = self.owned_projects | self.public_projects
        self.inaccessable_projects = (Project.objects.all()).difference(self.accessable_projects) 
        
        
    def Perform_Test(self,loginPayload,prjID):
        
        response_login = globalPerformLogin(loginPayload,"test_case_project_delete")
        
        factory_official = APIRequestFactory()
        user_view_official = ProjectDetail.as_view()
        theURL = f"http://127.0.0.1:8000/api/projects/{prjID}"
        
        request_official = factory_official.delete(theURL, loginPayload, format='json', HTTP_AUTHORIZATION=f"Bearer {response_login.data['access']}")
        response_official = user_view_official(request_official,pk=prjID)

        return response_official
    
    
    def test_case_remove_ownedprj(self):
        
        theID = (self.owned_projects.order_by('?')[0]).id
        response = self.Perform_Test(self.login_payload,theID)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    
    def test_case_remove_unownedprg(self):
        
        random_index = random.randint(1,len(self.inaccessable_projects)-1)
        theID = self.inaccessable_projects[random_index].id
        response = self.Perform_Test(self.login_payload,theID)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class test_case_project_history(APITestCase):
    
    @classmethod
    def setUpTestData(self):
        
        call_command("seed", verbosity=0)
        
        self.random_user = User.objects.order_by('?')[0]
        self.login_payload = {
            "email":f"{self.random_user.email}",
            "password":"defaultpassword"
        }
        self.owned_projects = Project.objects.filter(owner=self.random_user.id)
        self.unowned_projects = (Project.objects.all()).difference(self.owned_projects) 
        
        
    def Perform_Test(self,loginPayload,prjID):
        
        response_login = globalPerformLogin(loginPayload,"test_case_project_delete")
        
        factory_official = APIRequestFactory()
        user_view_official = ProjectHistoryDetail.as_view()
        theURL = f"http://127.0.0.1:8000/api/projects/{prjID}/history"
        
        request_official = factory_official.get(theURL, loginPayload, format='json', HTTP_AUTHORIZATION=f"Bearer {response_login.data['access']}")
        response_official = user_view_official(request_official,pk=prjID)

        return response_official
    
    
    def test_case_owned_project_history(self):
        
        theID = (self.owned_projects.order_by('?')[0]).id
        response = self.Perform_Test(self.login_payload,theID)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_case_unowned_project_history(self):
        
        random_index = random.randint(1,len(self.unowned_projects)-1)
        theID = self.unowned_projects[random_index].id
        response = self.Perform_Test(self.login_payload,theID)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)