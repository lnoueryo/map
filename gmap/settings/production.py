from .base import *
import environ

# SECURITY WARNING: keep the secret key used in production secret!
env = environ.Env()
env.read_env(os.path.join(BASE_DIR,'.env'))
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