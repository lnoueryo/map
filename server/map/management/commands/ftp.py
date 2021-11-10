import ftplib
import logging
import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

# logの設定
logger = logging.getLogger(__name__)
formatter = '%(asctime)s:%(name)s:%(levelname)s:%(message)s'
logging.basicConfig(
    filename=os.path.join(settings.BASE_DIR / f'log/ftp/log.txt'),
    level=logging.DEBUG,
    format=formatter
)
logger.setLevel(logging.INFO)

hostname = settings.FTP['HOST_NAME']
username = settings.FTP['USER_NAME']
password = settings.FTP['PASSWORD']
upload_src_path = os.path.join(settings.BASE_DIR / f'dist')
port = 21
timeout = 50


def ftp_upload(hostname, username, password, port, upload_src_path, upload_dst_path, timeout):
    logger.info({
        'action': 'ftp_upload',
        'status': 'run'
    })
    # FTP接続/アップロード
    with ftplib.FTP() as ftp:
        try:
            ftp.connect(host=hostname, port=port, timeout=timeout)
            # パッシブモード設定
            ftp.set_pasv("true")
            # FTPサーバログイン
            ftp.login(username, password)
            # deploy場所まで移動
            ftp.cwd("./www/map")
            placeFiles(ftp, upload_src_path)

        except ftplib.all_errors as e:
            logger.error({
                'action': 'ftp_upload',
                'message': 'FTP error = %s' % e
            })
    logger.info({
        'action': 'ftp_upload',
        'status': 'success'
    })

def execute():
    logger.info("===START FTP===")
    ftp_upload(hostname, username, password, port, upload_src_path, upload_src_path, timeout)
    logger.info("===FINISH FTP===")

def placeFiles(ftp, path):
    for name in os.listdir(path):
        localpath = os.path.join(path, name)
        print(ftp.pwd())
        if os.path.isfile(localpath):
            print("STOR", name, localpath)
            ftp.storbinary(f'STOR {name}', open(localpath,'rb'))
        elif os.path.isdir(localpath):
            print("MKD", name)
            try:
                ftp.mkd(name)

            # ignore "directory already exists"
            except Exception as e:
                print(e)
            print(ftp.pwd())
            print("CWD", name)
            ftp.cwd(name)
            placeFiles(ftp, localpath)
            print("CWD", "..")
            ftp.cwd("..")


class Command(BaseCommand):
    def handle(self, *args, **options):
        execute()