from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-waw-&0h%wa96+60qmg00%zrsz1()ro2t9i4k9)f)yzs1(5&f2%"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lunaluxio',
        'USER': 'lunalux',
        'PASSWORD': "EDj4kf2Sr9EML35",  # os.environ.get("dbpass"),
        'HOST': 'bacayo.iad1-mysql-e2-2a.dreamhost.com',
        'PORT': '3306',
    }
}


try:
    from .local import *
except ImportError:
    pass
