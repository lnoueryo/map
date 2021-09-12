from subprocess import PIPE, Popen, run
import os
import time
import signal
import json

import git
import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from gmap import ftp

def execute(message, description, branch):

    try:
        if os.getcwd() == 'D:\project\map\gmap\client':
            os.chdir('../')
        os.chdir('./client')
        nuxt = Popen(['yarn', 'generate'], stdin=PIPE, stdout=PIPE, shell=True)
        nuxt.wait()
        os.chdir('../')
        process1 = Popen(['echo' , 'yes', '&', 'echo', 'yes' '|', 'python3', '-m', 'pip', 'freeze', '>', 'requirements.txt'], stdin=PIPE, stdout=PIPE, shell=True)
        process1.wait()
        process1.kill()
        process2 = Popen(['echo' , 'yes', '&', 'echo', 'yes' '|', 'python3', 'manage.py', 'collectstatic'], stdin=PIPE, stdout=PIPE, shell=True)
        process2.wait()
        process2.kill()
        ftp.ftp_upload()
        repo = git.Repo()
        try:
            o = repo.remotes.origin
            o.pull()
            repo.git.add('--all')
            repo.git.commit('.','-m',f'{message}')
            o.push()
            create_pull_request(title=f'{message}', description=f'{description}', head_branch=f'{branch}')

        except Exception as e:
            print(e)
    except Exception as e:
        print(e)

def create_pull_request(title, description, head_branch, project_name='lnoueryo', repo_name='map', base_branch='develop'):
    """Creates the pull request for the head_branch against the base_branch"""
    git_pulls_api = "https://api.github.com/repos/{0}/{1}/pulls".format(
        project_name,
        repo_name)
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": "token {0}".format(settings.GIT_HUB['API_KEY']),
        "Content-Type": "application/json"}

    payload = {
        "title": title,
        "body": description,
        "head": head_branch,
        "base": base_branch,
    }

    r = requests.post(
        git_pulls_api,
        headers=headers,
        data=json.dumps(payload))

    if not r.ok:
        print("Request Failed: {0}".format(r.text))

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('message', type=str, default='')
        parser.add_argument('description', type=str, default='')
        parser.add_argument('branch', type=str, default='feature/new_page')

    def handle(self, *args, **options):
        message = options['message']
        description = options['description']
        branch = options['branch']
        execute(message, description, branch)