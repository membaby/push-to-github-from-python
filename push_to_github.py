import base64
from github import Github # pip install pygithub
from github import InputGitTreeElement
import os

ACCESS_TOKEN = 'GITHUB_ACCESS_TOKEN' #Generate from https://github.com/settings/tokens
REPO_NAME = 'REPOSITORY_NAME' # Existing repository name 
COMMIT_MSG = 'Automatic Commit' # Commitment Message Text
entry = r'PATH_TO_FILE'

g = Github(ACCESS_TOKEN)
repo = g.get_user().get_repo(REPO_NAME)

commit_message = COMMIT_MSG
master_ref = repo.get_git_ref('heads/main')
master_sha = master_ref.object.sha
base_tree = repo.get_git_tree(master_sha)

element_list = list()
with open(entry) as input_file:
    data = input_file.read()
element = InputGitTreeElement('articles/'+entry.split(os.sep)[-1], '100644', 'blob', data)
element_list.append(element)

tree = repo.create_git_tree(element_list, base_tree)
parent = repo.get_git_commit(master_sha)
commit = repo.create_git_commit(commit_message, tree, [parent])
master_ref.edit(commit.sha)