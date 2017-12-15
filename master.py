from flask import Flask, request, jsonify
from time import time
from pygit2 import Repository, clone_repository

app = Flask(__name__)

# store results that are sent to this url
@app.route('/results', methods=['POST'])
def store_result():
    result = request.json
    result_list.append(result)
    return 'Data recvd'


# pulls repo from url and stores clone
def set_repo():
  try:
    reposito = Repository('./repo')
  except:
    repository_url = 'https://github.com/robin70001/DFS1.git'
    repository_path = './repo'
    reposito = clone_repository(repository_url, repository_path)
  return reposito

# give work to any worker who access the url
@app.route('/work' , methods=['GET'])
def give_work():
    repository = set_repo()
    commits = get_commits(repository)
    global newtask

    try:
        commit_hash = commits[newtask]
        newtask = newtask + 1
        if newtask == 350:
            end_time = time() - timestr
            print(end_time)
            # print(result_list) # prints the result list containing the cyclomatic complexity of the py files in the commits
        return jsonify({'commit': str(commit_hash.id), 'id': newtask})
    except:
        return None

# walk through commits in the given repo and store in list
def get_commits(repositry):
  num_commits = []
  for num_commit in repositry.walk(repositry.head.target):
    num_commits.append(repositry.get(num_commit.id))
  return num_commits


if __name__ == '__main__':
    newtask = 0
    timestr = time()
    global result_list
    result_list = []
    app.run(threaded=True, debug=True)