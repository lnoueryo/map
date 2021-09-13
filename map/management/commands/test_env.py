from subprocess import PIPE, Popen, run
import os

from django.core.management.base import BaseCommand, CommandError
from gmap import ftp

def execute():

    try:
        if os.getcwd() == 'D:\project\map\gmap\client':
            os.chdir('../')
        os.chdir('./client')
        nuxt = Popen(['yarn', 'generate'], stdin=PIPE, stdout=PIPE, shell=True)
        nuxt.wait()
        os.chdir('../')
        ftp.ftp_upload()
    except Exception as e:
        print(e)


class Command(BaseCommand):
    def handle(self, *args, **options):
        execute()