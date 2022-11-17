from rest_framework_simplejwt.tokens import RefreshToken
import os
import shutil
import git
from git import Actor

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

def rename_dir_for_user(oldname, newname):
    '''Rename the directory upon changing the user email'''
    try:
        if(os.path.exists(f"/home/API-Builder/{oldname}")):
            os.rename(f"/home/API-Builder/{oldname}", f"/home/API-Builder/{newname}")
        else:
            print(f"User {oldname} does not have any directories!")
    except OSError as error:
        print(error)
        
        
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
        
def rename_dir_for_project_of_user(TheEmailOfuser, oldname, newname):
    '''Rename the directory upon changing the user email'''
    try:
        if(os.path.exists(f"/home/API-Builder/{TheEmailOfuser}/{oldname}")):
            os.rename(
                f"/home/API-Builder/{TheEmailOfuser}/{oldname}", 
                f"/home/API-Builder/{TheEmailOfuser}/{newname}"
            )
        else:
            print(f"/home/API-Builder/{TheEmailOfuser}/{oldname}  (DOES NOT EXIST!)")
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


#####################       PYGIT2 CHANGES       #####################


def initialize_localrepo (TheEmailOfuser,ProjectName):
    '''Initializes a localrepo inside the project folder, requires email and project name'''
    
    repo_dir = f"/home/API-Builder/{TheEmailOfuser}/{ProjectName}"
    
    if(not os.path.isdir(repo_dir+"/.git")):
        repo = git.Repo.init(repo_dir)
    else:
        print("Local repo already exists!")


def get_history_of_repo (TheEmailOfuser,ProjectName):
    '''Gets the history of the repo, returns a list containing dictionaries, requires email and project name'''

    repo_dir = f"/home/API-Builder/{TheEmailOfuser}/{ProjectName}"
    
    if(os.path.isdir(repo_dir+"/.git")):
        
        repo = git.Repo(repo_dir)
        
        Log = repo.git.log('--pretty=format:%h</^-^\>%an</^-^\>%ae</^-^\>%aD</^-^\>%ar</^-^\>%s')
        theChanges_aslists = Log.split("\n")
        listOfChanges = []

        for theChange in theChanges_aslists:
            
            DetailedChange = theChange.split("</^-^\>")
            theDictionary = {
                "Hash":"",
                "Author":"",
                "AuthorEmail":"",
                "Time":"",
                "TimeAgo":"",
                "Commit Message":""
            }
            
            for value, dictionaryKey in zip(DetailedChange,theDictionary): 
                theDictionary[dictionaryKey] = value
                
            listOfChanges.append(theDictionary)
            
        return listOfChanges
        
    else:
        print(f"Repo in: {repo_dir} does not exist!")
        return
    
    
def commit_repo_changes (TheEmailOfuser,userName,ProjectName):
    '''Commits the changes made by the user, requires email, name, and project name' '''
    
    repo_dir = f"/home/API-Builder/{TheEmailOfuser}/{ProjectName}"
    
    if(os.path.isdir(repo_dir+"/.git")):
        
        repo = git.Repo(repo_dir)
        repo.index.add('**')
        author = Actor(userName,TheEmailOfuser)
        repo.index.commit("User made changes", author=author)
        
    else:
        print(f"Repo in: {repo_dir} does not exist!") 
