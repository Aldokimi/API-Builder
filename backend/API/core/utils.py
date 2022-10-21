from rest_framework_simplejwt.tokens import RefreshToken
import os
import shutil

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def make_dir_for_user(TheEmailOfuser):
    '''Creates a directory for the user to put the projects inside when registering, requires email'''
   
    try:
        
        if(not os.path.exists("/home/API-Builder")):
            os.mkdir(f"/home/API-Builder")
        
        os.mkdir(f"/home/API-Builder/{TheEmailOfuser}")
        
    except OSError as error:
        print (error)
        
        
def remove_dirs_of_user(TheEmailOfuser):
    '''Removes all directories associated with the user, requires email'''
    
    try:
        if(os.path.exists(f"/home/API-Builder/{TheEmailOfuser}")):
            shutil.rmtree(f"/home/API-Builder/{TheEmailOfuser}")
        else:
            print(f"User {TheEmailOfuser} does not have any directories!")
    except OSError as error:
        print(error)
        
        
def make_dir_for_project_of_user(TheEmailOfuser,ProjectName):
    '''Creates a directory for the given project, requires email and project name'''
    
    try:
        if(os.path.exists(f"/home/API-Builder/{TheEmailOfuser}/{ProjectName}")):
            print(f"User: '{TheEmailOfuser}' already has a directory under name: /home/API-Builder/{TheEmailOfuser}/{ProjectName}")
        else:
            os.mkdir(f"/home/API-Builder/{TheEmailOfuser}/{ProjectName}")
    except OSError as error:
        print(error)
        
        
def remove_dir_for_project_of_user(TheEmailOfuser,ProjectName):
    '''Removes the directory of the given project, requires email and project name'''
    
    try:
        if(os.path.exists(f"/home/API-Builder/{TheEmailOfuser}/{ProjectName}")):
            shutil.rmtree(f"/home/API-Builder/{TheEmailOfuser}/{ProjectName}")
        else:
            print(f"/home/API-Builder/{TheEmailOfuser}/{ProjectName}  (DOES NOT EXIST!)")
        
    except OSError as error:
        print(error)