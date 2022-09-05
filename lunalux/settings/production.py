from .base import *

DEBUG = True

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
root = "/home/kasfre2/lunalux.io/public"
STATIC_ROOT = os.path.join(root, "static")
MEDIA_ROOT = os.path.join(root, "media")


try:
    from .local import *
except ImportError:
    pass
