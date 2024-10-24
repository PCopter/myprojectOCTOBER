from pathlib import Path
from dotenv import load_dotenv
import os
from celery.schedules import crontab

load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG") == "True"

production_host = os.getenv("PRODUCTION_HOST")
# ALLOWED_HOSTS = [production_host] if production_host is not None else ["127.0.0.1"]

# IPv4 Address --> 10.236.126.195:8000 (WIFI - InternetMGMT)
ALLOWED_HOSTS = ['localhost', '127.0.0.1','10.236.35.235']



# Application definition

INSTALLED_APPS = [
    'app_users.apps.AppUsersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_general.apps.AppGeneralConfig',
    'app_certifications.apps.AppCertificationsConfig',
    'app_standard.apps.AppStandardConfig',
    'app_regulation.apps.AppRegulationConfig',
    'django_celery_beat',
    'django_celery_results',
    'ckeditor',
    'app_taskschedule.apps.AppTaskscheduleConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': os.getenv('DB_NAME') ,
        'USER' : os.getenv('DB_USER'),
        'PASSWORD' : os.getenv('DB_PASSWORD'),
        'HOST' : os.getenv('DB_HOST'),
        'PORT' : os.getenv('DB_PORT')
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Bangkok'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = "static/"
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Auth
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
LOGIN_URL = "login"


AUTH_USER_MODEL = "app_users.CustomUser"
AUTHENTICATION_BACKENDS = [
    "app_users.utils.auth_email_backend.EmailBackend",
    "django.contrib.auth.backends.ModelBackend"
]
        
#Email
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
# EMAIL_HOST_USER = 'copter.phanuwat@gmail.com'
# EMAIL_HOST_PASSWORD = 'hxsh xxgz ktgj gslu' 
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

#Email ใช้ภายในเครือข่ายบริษัท
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '10.236.36.50'
EMAIL_PORT = 25
EMAIL_USE_TLS = False # ขึ้นอยู่กับการตั้งค่าเซิร์ฟเวอร์ภายใน
EMAIL_USE_SSL = False # ขึ้นอยู่กับการตั้งค่าเซิร์ฟเวอร์ภายใน
EMAIL_HOST_USER = '' # หากไม่ต้องการการตรวจสอบสิทธิ์ สามารถเว้นว่างได้
EMAIL_HOST_PASSWORD = '' # หากไม่ต้องการการตรวจสอบสิทธิ์ สามารถเว้นว่างได้
DEFAULT_FROM_EMAIL = 'MCP-QA-WEB@MCP.MEAP.COM'

# EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# EMAIL_FILE_PATH = BASE_DIR / "test_inbox"
# PASSWORD_RESET_TIMEOUT = 600

# Celery Setting
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json' 
CELERY_TIMEZONE = 'Asia/Bangkok'

# Celery Beat
# CELERY_BEAT_SCHEDULE = {
#     'send-weekly-email-certifications': {
#         'task': 'app_certifications.tasks.send_weekly_email',
#         'schedule': crontab(day_of_week='friday', hour=8, minute=30),
#     },
#     'send-weekly-email-regulations': {
#         'task': 'app_regulation.tasks.send_weekly_email',
#         'schedule': crontab(day_of_week='monday', hour=14, minute=37), 
#     },
#     # monthly
# }

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'




