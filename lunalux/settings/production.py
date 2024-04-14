from .base import *

DEBUG = False

# change this
SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = ["*", "lunalux.io"]
CSRF_TRUSTED_ORIGINS = ['*','https://lunalux.io']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lunaluxio',
        'USER': 'lunalux',
        'PASSWORD': os.environ.get("dbpass"),
        'HOST': 'bacayo.iad1-mysql-e2-2a.dreamhost.com',
        'PORT': '3306',
    }
}



# change these to fit.
root = "/home/kasfre2/cdn.lunalux.io/public"
STATIC_ROOT = os.path.join(root, "static")
MEDIA_ROOT = os.path.join(root, "media")

STATIC_URL = 'https://cdn.lunalux.io/static/'
MEDIA_URL = 'https://cdn.lunalux.io/media/'


try:
    from .local import *
except ImportError:
    pass
