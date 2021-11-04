from .base import *
import io
import sqlalchemy as sa
import pymysql
import google.auth
import environ
from google.cloud import secretmanager

env = environ.Env(DEBUG=(bool, False))
env_file = os.path.join(BASE_DIR, ".env")

# Attempt to load the Project ID into the environment, safely failing on error.
try:
    _, os.environ["GOOGLE_CLOUD_PROJECT"] = google.auth.default()
except google.auth.exceptions.DefaultCredentialsError:
    pass
# print(os.environ.get("GOOGLE_CLOUD_PROJECT", None))
if os.path.isfile(env_file):
    env.read_env(env_file)
else:
    try:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/gmap-keys/versions/latest"
        payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")

        env.read_env(io.StringIO(payload))
    except Exception as e:
        print(e)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# API_KEY
YAHOO = {'API_KEY': env('YAHOO_API_KEY')}

TWITTER = {
    'API_KEY': env('TWITTER_API_KEY'),
    'API_SECRET_KEY': env('TWITTER_API_SECRET_KEY'),
    'ACCESS_TOKEN': env('TWITTER_ACCESS_TOKEN'),
    'ACCESS_TOKEN_SECRET': env('TWITTER_ACCESS_TOKEN_SECRET'),
}

GOOGLE = {
    'GOOGLE_MAPS': {
        'API_KEY': env('GOOGLE_MAPS_API_KEY')
    }
}

# mysql
DATABASE = {
    'ENGINE': env('DATABASE_ENGINE'),
    'NAME': env('DATABASE_NAME'),
    'USER': env('DATABASE_USER'),
    'HOST': env('DATABASE_HOST'),
    'PASSWORD': env('DATABASE_PASSWORD'),
}

db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
cloud_sql_connection_name = 'trim-tide-313616:asia-northeast1:gmap'
db_config = {
    "pool_size": 5,
    "max_overflow": 10,
    "pool_timeout": 30,  # 30 seconds
    "pool_recycle": 3600,  # 30 minutes
    "pool_pre_ping": True
}
ENGINE = sa.create_engine(sa.engine.url.URL(
    drivername="mysql+pymysql",
    username=DATABASE["USER"],
    password=DATABASE["PASSWORD"],
    database=DATABASE["NAME"],
    query={
        "unix_socket": "{}/{}".format(
            db_socket_dir,  # e.g. "/cloudsql"
            cloud_sql_connection_name)  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
    }
), **db_config)
