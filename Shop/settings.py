"""
Django settings for Shop project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)3*e*46j$d7zio(i_9og_zde@m7(@&_5*knm&h)06-t+ivw5jx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
# in django db is created for apps automatically, except messages and staticfiles 
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local Apps
    'accounts.apps.AccountsConfig',
    'home.apps.HomeConfig',
    'orders.apps.OrdersConfig',

    # Third Party Apps
    'storages',
    'django_celery_beat',
    'ckeditor'
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

ROOT_URLCONF = 'Shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'orders.context_processors.cart_context_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'Shop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

#### to use other database ####

# install postgresql
# pip install psycopg2 or psycopg2-binary

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME':  'name',
#         'USER': 'username',
#         'PASSWORD': 'password',
#         'HOST': '1270.0.1',
#         'PORT': '5432'
#     }
# }


#### using cache 
## it is used instaed server in session, (by default saved in db in server and a hashcode in client)
# install redis package in linux
# pip install redis
# pip install hiredis

#  
# cache_db saves in db too,
# in reading first, try to read from cache then db






# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# set the timezone, recommended
TIME_ZONE = 'Asia/Tehran'
## setting the TIME_ZONE is not enough, use pytz in datetimes in code

USE_I18N = True


# if USE_TZ is False, django use the system timezone, not recommended
USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# whole static file that isnt related to specific app, like jumbotron
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# to use media file:
MEDIA_URL = '/media/'  # read from root of app in media file (to get media)
MEDIA_ROOT = BASE_DIR / 'media' # when you upload a media, a media dir create, and store the media there





# notify the django from new User model
# AUTH_USER_MODEL = "myapp.MyUserModel" # dont use module name
AUTH_USER_MODEL = "accounts.User"



#****************************************
#** to connect to CDN for media files ***
#****************************************

# it saves the media file in CDN not in /media/

# 2 way to connect cnd, 1)automatically 2)manually(using celery)

# pip install django-storages
# pip install boto3
# add 'storages' in installed app in setting.py

# required
#automatically
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = '01546184-771b-4f0e-b4c8-2dac8f08b385'
AWS_SECRET_ACCESS_KEY = '163d2838947ca0dc0db044e27e6cce0f0c94eeb71f618f6b1437a0b3a602748b'
AWS_S3_ENDPOINT_URL = 'https://s3.ir-thr-at1.arvanstorage.ir'
AWS_STORAGE_BUCKET_NAME = 'django-shop-train'
# optinal
AWS_SERVICE_NAME = 's3'# required for manully mode
AWS_S3_FILE_OVERWRITE = False   # overwrite the same name files

AWS_LOCAL_STORAGE = f'{BASE_DIR}/aws/' # where to download files





CCKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Basic',
    },
}