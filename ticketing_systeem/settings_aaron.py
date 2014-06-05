""" @author: 'bartsteverink' """

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ticketing',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': '',
    }
}

PDF_LOCATION = 'C:\Users\Aaron'
ADMIN_MEDIA_PREFIX = '/static/admin/'

ALLOWED_HOSTS = [
    'ticketing.local'
]

INTERNAL_IPS = ('127.0.0.1',)
