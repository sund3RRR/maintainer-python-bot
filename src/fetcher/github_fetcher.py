import os
from github import Github, Auth


auth = Auth.Token(os.environ["githubToken"])
g = Github(auth=auth)