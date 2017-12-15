from radon.metrics import mi_visit
from radon.complexity import cc_visit, cc_rank
from pygit2 import Repository, clone_repository
import requests

def set_repo():
  try:
    repo = Repository('./repo')
  except:
    repository_url = 'https://github.com/robin70001/DFS1.git'
    repository_path = './repo'
    repo = clone_repository(repository_url, repository_path)
  return repo

# ask for work from the given iurl
def get_work(repo):
  response = requests.get('http://127.0.0.1:5000/work', params={'key': 'value'})
  response.encoding = 'utf-8'
  json_file = response.json()
  data_tr = repo.get(json_file['commit']).tree
  id = json_file['id']
  sources = get_data(data_tr, repo)
  files = extract_files(sources)
  return files, id
  
# stores data into a list
def get_data(list_tr, repo):
  sources = []
  for entry in list_tr:
    if ".py" in entry.name:
      sources.append(entry)
      if "." not in entry.name:
        if entry.type == 'tree':
          new_tree = repo.get(entry.id)
          sources += (get_data(new_tree, repo))
  return sources

# complexity calculate
def start_work(work):
  results = []
  for file in work:
    results.append(compute_complexity(file))
  return results
  
# cyclomatic complexity calculation for th files provided
def compute_complexity(source):
  result =[]
  blocks = cc_visit(source)
  mix_path = mi_visit(source, True)
  for func in blocks:
    result.append(func.name+": Rank:"+cc_rank(func.complexity))
  return result

# post results to the url 
def output_final(result):
  result = {'Result' : result}
  post = requests.post('http://127.0.0.1:5000/results', json=result)

# decodes the files stored in the list
def extract_files(sources):
    files = []
    for source in sources:
      files.append(repository[source.id].data.decode("utf-8"))
    return files


if __name__ == '__main__':
    bool = True
    while bool:
      repository = set_repo()
      work, id = get_work(repository)
      print(id)
      if id > 350:
        bool = False
        print("Process Terminated")
      finalop = start_work(work)
      output_final(finalop)