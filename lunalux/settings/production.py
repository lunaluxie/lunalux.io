from .base import *

DEBUG = False

# change this
SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = ["lunalux.io"]
CSRF_TRUSTED_ORIGINS = ['https://lunalux.io']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get("dbname"),
        'USER': os.environ.get("dbuser"),
        'PASSWORD': os.environ.get("dbpass"),
        'HOST': os.environ.get("dbhost"),
        'PORT': int(os.environ.get("dbport")),
    }
}



# change these to fit.
HOME = os.environ.get("HOME")
root = os.path.join(HOME,"/cdn.lunalux.io/public")
STATIC_ROOT = os.path.join(root, "static")
MEDIA_ROOT = os.path.join(root, "media")

STATIC_URL = 'https://cdn.lunalux.io/static/'
MEDIA_URL = 'https://cdn.lunalux.io/media/'


try:
    from .local import *
except ImportError:
    pass
