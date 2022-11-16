from rest_framework_simplejwt.tokens import RefreshToken
import os
import shutil
import pygit2
from datetime import datetime, timezone, timedelta


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
        print ('make_dir_for_user:',error)
        
        
def remove_dirs_of_user(TheEmailOfuser):
    '''Removes all directories associated with the user, requires email'''
    
    try:
        if(os.path.exists(f"/home/API-Builder/{TheEmailOfuser}")):
            shutil.rmtree(f"/home/API-Builder/{TheEmailOfuser}")
        else:
            print(f"(remove_dirs_of_user): User {TheEmailOfuser} does not have any directories!")
    except OSError as error:
        print('remove_dirs_of_user:',error)
        
        
def make_dir_for_project_of_user(TheEmailOfuser,ProjectName):
    '''Creates a directory for the given project, requires email and project name'''
    
    try:
        if(os.path.exists(f"/home/API-Builder/{TheEmailOfuser}/{ProjectName}")):
            print(f"(make_dir_for_project_of_user): User '{TheEmailOfuser}' already has a directory under name: /home/API-Builder/{TheEmailOfuser}/{ProjectName}")
        else:
            os.mkdir(f"/home/API-Builder/{TheEmailOfuser}/{ProjectName}")
    except OSError as error:
        print('make_dir_for_project_of_user:',error)
        
        
def remove_dir_for_project_of_user(TheEmailOfuser,ProjectName):
    '''Removes the directory of the given project, requires email and project name'''
    
    try:
        if(os.path.exists(f"/home/API-Builder/{TheEmailOfuser}/{ProjectName}")):
            shutil.rmtree(f"/home/API-Builder/{TheEmailOfuser}/{ProjectName}")
        else:
            print(f"(remove_dir_for_project_of_user): /home/API-Builder/{TheEmailOfuser}/{ProjectName}  (DOES NOT EXIST!)")
        
    except OSError as error:
        print('remove_dir_for_project_of_user:',error)
    
          
def initialize_localrepo (TheEmailOfuser,ProjectName):
    '''Initializes a localrepo inside the project folder, requires email and project name'''
    
    repo_dir = f"/home/API-Builder/{TheEmailOfuser}/{ProjectName}"
    
    if(not os.path.isdir(repo_dir+"/.git")):
        repo = pygit2.init_repository(repo_dir, initial_head='master')
    else:
        print("(initialize_localrepo): Local repo already exists!")


def get_history_of_repo (TheEmailOfuser,ProjectName):
    '''Gets the history of the repo, returns a JSON containing dictionaries, requires email and project name'''

    repo_dir = f"/home/API-Builder/{TheEmailOfuser}/{ProjectName}"
    
    if(os.path.isdir(repo_dir+"/.git")):
        
        repo = pygit2.Repository(repo_dir)
        theDictionary = {}
        
        commits = repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL)
        sum_commits = 0
        for c in commits: sum_commits+=1
        
        for commit in repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL):
            
            the_author = commit.author
            tzinfo = timezone( timedelta(minutes=the_author.offset) )
            dt = datetime.fromtimestamp(float(the_author.time), tzinfo)
            timestr = dt.strftime('%c %z')
            order = f'Commit# {sum_commits}'
            msg = commit.message.strip('\n')
            
            dic = {
                "Hash":f"{commit.hex}",
                "Author":f"{the_author.name}",
                "AuthorEmail":f"{the_author.email}",
                "Time":f"{timestr}",
                "Commit Message":f"{msg}"
            }
        
            theDictionary[order] = dic
            sum_commits-=1
            
        return theDictionary
        
    else:
        print(f"(get_history_of_repo): Repo in: {repo_dir} does not exist!")
        return {}
    
    
def commit_repo_changes (TheEmailOfuser,userName,ProjectName):
    '''Commits the changes made by the user, requires email, name, and project name' '''
    
    repo_dir = f"/home/API-Builder/{TheEmailOfuser}/{ProjectName}"
    
    if(os.path.isdir(repo_dir+"/.git")):
        
        repo = pygit2.Repository(repo_dir)
        (index := repo.index).add_all()
        index.write()
        tree = index.write_tree()
        author = pygit2.Signature(userName,TheEmailOfuser)
        committer = pygit2.Signature(userName,TheEmailOfuser)
        message = "User made changes"
        
        #Safety check incase this is the first commit:
        try:
            tmp = repo.head.target # this can raise an error if this is the very first commit
            repo.create_commit("HEAD", author, committer, message, tree, [repo.head.target])
        except pygit2.GitError:
            repo.create_commit("HEAD", author, committer, message, tree, [])
        
    else:   #changing the directory name
        print(f"(commit_repo_changes): Repo in: {repo_dir} does not exist!") 
