import os
from .settings import BASE_DIR

# Make this unique, and don't share it with anybody.
# http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = 'MylongSecretkey1234567890'


# Email Server Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'stevebarriya25287@gmail.com'
SERVER_EMAIL = 'stevebarriya25287@gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'stevebarriya25287@gmail.com'
EMAIL_HOST_PASSWORD = 'sam@#777'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False


# Database Settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'temp.sqlite3'),
    }
}

# Server Customizations
ADMIN_EMAIL = "stevebarriya25287@gmail.com"
URL_FOR_LINKS = "https://crm.example.com"


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True
