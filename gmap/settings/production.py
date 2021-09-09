from .base import *
import io

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