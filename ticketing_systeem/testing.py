__author__ = 'Aaron'

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
        'USER': 'ticketing',
        'PASSWORD': 'geheim',
    }
}

PDF_LOCATION = '/home/ec2-user/Sites/ticketing/files'
ADMIN_MEDIA_PREFIX = '/static/admin/'

ALLOWED_HOSTS = [
    'ticketing.in2systems.nl'
]

SITE_ROOT = 'http://ticketing.in2systems.nl'
#Mollie settings
MOLLIE_REPORT_URL = SITE_ROOT + '/events/%s/step4'

#INTERNAL_IPS = ('127.0.0.1',)
