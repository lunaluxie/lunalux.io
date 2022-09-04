from .base import *

DEBUG = False

# change this
SECRET_KEY = "django-insecure-waw-&0h%wa96+60qmg00%zrsz1()ro2t9i4k9)f)yzs1(5&f2%"

ALLOWED_HOSTS = ["*"]


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
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


try:
    from .local import *
except ImportError:
    pass
