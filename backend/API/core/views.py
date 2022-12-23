
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Project
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.parsers import JSONParser

from .serializers import CreateUserSerializer, UpdateUserSerializer, \
     RegistrationSerializer, PasswordChangeSerializer,\
        CreateProjectSerializer, UpdateProjectSerializer
from . import utils
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
import os

# Authentication views
class RegistrationView(APIView):
    def post(self, request):
        '''Creates user + their own directory'''
        
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            utils.make_dir_for_user(serializer.data['email'])
            return Response({"message":"Successfully logged in", **serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    parser_classes = [JSONParser]
    def post(self, request):
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)

        email = request.data.get('email', False)
        password = request.data.get('password', 'ERROR')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            auth_data = utils.get_tokens_for_user(request.user)
            auth_data['id'] = request.user.id
            auth_data['email'] = request.user.email
            auth_data['username'] = request.user.username
            auth_data['csrftoken'] = request.META.get('CSRF_COOKIE', None)
            return Response({'msg': 'Login Success', **auth_data}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True) 
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Permission classes
class IsProjectOwner(BasePermission):
    # for view permission
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    # for object level permissions
    def has_object_permission(self, request, view, vacation_obj):
        return vacation_obj.owner.id == request.user.id

# User requests handling 
class UserList(APIView):
    """
    List all users, or create a new user.
    """
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = CreateUserSerializer(users, many=True)
        return Response(serializer.data)

class UserDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    permission_classes = [IsAuthenticated, ]
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateUserSerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return UpdateUserSerializer

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = CreateUserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        
        user = self.get_object(pk)
        if user.id is not self.request.user.id:
            raise PermissionDenied()
        my_serializer = self.get_serializer_class()
        serializer = my_serializer(user, data=request.data)
        if serializer.is_valid():
            try:
                if "username" in request.data:  #Existing user check
                   for aUser in User.objects.all():
                       if(serializer.validated_data['username'] == aUser.username):
                           return Response({'msg': f"a User with the same username '{serializer.validated_data['username']}' already exists!"}, status=status.HTTP_400_BAD_REQUEST)
                if "email" in request.data:   #Existing email check
                    if(os.path.exists(f"/home/API-Builder/{serializer.validated_data['email']}")):
                        return Response({'msg': f"a User with the same email address '{serializer.validated_data['email']}' already exists!"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        if user.email != serializer.validated_data["email"]:
                            utils.rename_dir_for_user(user.email, serializer.validated_data["email"]) 
            except Exception as E:
                return Response({'msg': f"Unknown Exception happend, its value is: {E}"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        '''Deletes a user'''
        
        user = self.get_object(pk)
        if user.id is not self.request.user.id:
            raise PermissionDenied()
        utils.remove_dirs_of_user(user.email)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# User requests handling 
class ProjectList(APIView):
    """
    List all projects, or create a new Project.
    """
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateProjectSerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return UpdateProjectSerializer

    def get(self, request, format=None):
        '''This views all the projects of ALL users'''
        
        sameID = Project.objects.filter(owner=request.user.id)
        privates = Project.objects.filter(private=False)
        projects = sameID | privates
        serializer = CreateProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        '''This creates a project directory for a specific user'''
        my_serializer = self.get_serializer_class()
        project = my_serializer(data=request.data)
        if project.is_valid():
            if project.validated_data['owner'].id is not self.request.user.id:
                raise PermissionDenied()
            
            projects = Project.objects.filter(name=project.validated_data['name'])
            if (len(projects) != 0):
                return Response({
                    "message":"Project name exists!"
                }, status=status.HTTP_400_BAD_REQUEST)
            try:
                fileName = project.validated_data['file_name']  #User makes the file with a custom name
            except KeyError:
                fileName = "swc_"+project.validated_data['owner'].username
                project.file_name = fileName
                #Error return incase we decide to have fileName as mandatory
                #return Response({
                #    "message":"Project must have a file name!",
                #    "file_name": ["This field is required."]
                #}, status=status.HTTP_400_BAD_REQUEST)  
            utils.make_dir_for_project_of_user( project.validated_data['owner'].email , project.validated_data['name'] )
            utils.initialize_localrepo( project.validated_data['owner'].email , project.validated_data['name'] )
            project_loc = f"/home/API-Builder/{project.validated_data['owner'].email}/{project.validated_data['name']}"
            utils.create_file(project.validated_data['file_content'],project_loc,fileName,project.validated_data['file_type'])
            utils.commit_repo_changes( project.validated_data['owner'].email , project.validated_data['owner'].username ,project.validated_data['name'], f"Project: '{project.validated_data['name']}' initialization" ) 
            project.save()
            return Response(project.data, status=status.HTTP_201_CREATED)
        return Response(project.errors, status=status.HTTP_400_BAD_REQUEST)

# Project requests handling
class ProjectDetail(APIView):
    """
    Retrieve, update or delete a Project instance.
    """
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateProjectSerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return UpdateProjectSerializer

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        
        project = self.get_object(pk)
        if( (not project.private) or project.owner.email == request.user.email):
            serializer = CreateProjectSerializer(project)
            return Response(serializer.data)
        return Response({'msg': 'Unauthorized access!'}, status=status.HTTP_401_UNAUTHORIZED)
    
    
    def patch(self, request, pk, format=None):
        project = self.get_object(pk)
        my_serializer = self.get_serializer_class()
        serializer = my_serializer(project, data=request.data)
        if serializer.is_valid():
            try:
                check = False
                if "name" in request.data:
                    if project.name != serializer.validated_data["name"]:
                        if(os.path.exists(f"/home/API-Builder/{project.owner.email}/{serializer.validated_data['name']}")):
                            return Response({'msg': f"Project with the name '{serializer.validated_data['name']}' already exists for the user '{project.owner.email}' !"}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            utils.rename_dir_for_project_of_user(project.owner.email, project.name, serializer.validated_data["name"])
                            check = True
                if "file_content" and "file_type" in request.data:
                    if check:
                        FileLoc = f"/home/API-Builder/{project.owner.email}/{serializer.validated_data['name']}"
                    else:
                        FileLoc = f"/home/API-Builder/{project.owner.email}/{project.name}"
                    if "file_name" in request.data:
                        utils.update_file(serializer.validated_data["file_content"],FileLoc,serializer.validated_data["file_name"],serializer.validated_data["file_type"],project.file_name,project.file_type)
                    else:
                        utils.update_file(serializer.validated_data["file_content"],FileLoc,project.file_name,serializer.validated_data["file_type"],project.file_name,project.file_type)
                    name = project.owner.username
                    utils.commit_repo_changes( project.owner.email , name ,project.name ) 
            except Exception as E:
                return Response({'msg': f"Unknown Exception happend, its value is: ({E})"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        '''This deletes a certain project associated with a user'''
        
        project = self.get_object(pk)
        if project.owner.id is not self.request.user.id:
            raise PermissionDenied()
        utils.remove_dir_for_project_of_user(project.owner.email,project.name)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# History management

class ProjectHistoryDetail(APIView):
    """
    Get the history data of a project
    """
    permission_classes = [IsAuthenticated, ]
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        project = self.get_object(pk)
        
        if(project.owner.email == request.user.email):
            response_data = utils.get_history_of_repo(project.owner.email, project.name)
            return Response(response_data)
        return Response({'msg': 'Unauthorized access!'}, status=status.HTTP_401_UNAUTHORIZED)
    

class ProjectOldDataDetail(APIView):
    """
    Get the old file data of a project
    """
    permission_classes = [IsAuthenticated, ]
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404
    
    def get(self, request, pk ,hash, format=None):
        project = self.get_object(pk)
       
        if(project.owner.email == request.user.email):
            path = f"/home/API-Builder/{request.user.email}/{project.name}"
            response_data = utils.get_old_data_from_hash(hash, path)
            if(response_data[0]):
                #print("Data:",response_data[1])
                send = utils.handle_filecontent_for_output(response_data[1],response_data[2])
                return Response(send,status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'No such hash!'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': 'Unauthorized access!'}, status=status.HTTP_401_UNAUTHORIZED)