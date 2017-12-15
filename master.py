from flask import Flask, request, jsonify
from time import time
from pygit2 import Repository, clone_repository

app = Flask(__name__)
results = []
todo = 0

def set_repo():
    try:
        repo = Repository('./repo')
    except:
        repo_url = FLASK_SERVER_NAME
        repo_path = './repo'
        repo = clone_repository(repo_url, repo_path)
    return repo

def get_commits(repo):
    commits = []
    for commit in repo.walk(repo.head.target):
        commits.append(repo.get(commit.id))
    return commits

@app.route('/work' , methods=['GET'])
def task():
    repo = set_repo()
    commits = get_commits(repo)
   

    try:
        commit_hash = commits[todo]
        todo = todo + 1
        end_time = time() - start_time
        print(end_time)
        return jsonify({'commit': str(commit_hash.id), 'id': todo})
    except:
        return None

@app.route('/results', methods=['POST'])
def store_result():
    results.append(request.json)
    return 'Work done'

if __name__ == '__main__':
    start_time = time()
    app.run()