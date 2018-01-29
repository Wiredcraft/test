import json
import requests
import yaml
import os

token = os.environ.get('GITHUB_TOKEN')
if token == '':
    token = raw_input('Paste your GitHub token? (see https://github.com/settings/tokens): ')
    pass
repo = raw_input('Which repo do you want to setup? (e.g. Wiredcraft/test): ')

with open('labels.yml', 'r') as f:
  default_labels = yaml.load(f)

url = 'https://api.github.com/repos/' + repo + '/labels'
headers = {'Authorization': 'token %s' % token}

def get_labels():
  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status() # optional but good practice in case the call fails!
    return [label['name'] for label in response.json()]
  except Exception as e:
    return e

def set_labels(labels):
  for label in default_labels:
    try:
      # Label was in the list, we update GH
      labels.remove(label['name'])
      update_label(label)
    except ValueError:
      # Label wasn't in the array, we add it to GH
      create_label(label)

  # We now remove the labels left
  for label in labels:
     delete_label(label)

def update_label(label):
  print 'Update label (%s) on GH' % label['name']
  try:
    response = requests.patch(url + '/' + label['name'], data=json.dumps(label), headers=headers)
    response.raise_for_status()
    return response.json()
  except Exception as e:
    return e

def create_label(label):
  print 'Create label (%s) on GH' % label['name']
  try:
    response = requests.post(url, data=json.dumps(label), headers=headers)
    response.raise_for_status()
    return response.json()
  except Exception as e:
    return e

def delete_label(label):
  print 'Delete label (%s) from GH' % label
  try:
    response = requests.delete(url + '/' + label, headers=headers)
    response.raise_for_status()
    return response.json()
  except Exception as e:
    return e

labels = get_labels()
set_labels(labels)
