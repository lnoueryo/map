from subprocess import PIPE, Popen, run
import os
import time
import signal
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

def execute():

    try:
        if os.getcwd() == 'D:\project\map\gmap\client':
            os.chdir('../')

        # process = Popen(['echo' , 'yes', '&', 'echo', 'yes' '|', 'python3', '-m', 'pip', 'freeze', '>', 'requirements.txt'], stdin=PIPE, stdout=PIPE, shell=True)
        # process = Popen(['echo' , 'yes', '&', 'echo', 'yes' '|', 'python3', 'manage.py', 'collectstatic'], stdin=PIPE, stdout=PIPE, shell=True)
        # print(process)
        # process.wait()
        # process.kill()

        # process = Popen(settings.GCLOUD_BUILD, stdin=PIPE, stdout=PIPE, shell=True)
        # print(process)
        # time.sleep(300)
        # process.kill()

        process = Popen(settings.GCLOUD_DEPLOY, stdin=PIPE, stdout=PIPE, shell=True)
        process.wait()
        process.kill()
    except Exception as e:
        print(e)

class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument('file', nargs='?', default='json', type=str)

    def handle(self, *args, **options):
        execute()