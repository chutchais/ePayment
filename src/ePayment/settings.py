"""
Django settings for ePayment project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()


import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '(ixqqurv5j_oigrl(ggh(fbj(7f3@rw5dec%#e1k3-hbz&7o_8'
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'debug_toolbar',
    'crispy_forms',
    'user_profile',
    'tariff',
    'tax',
    'oog',
    'booking',
    'order',
    'bl',
    'orderimport',
    'import_export',
    'shorepass',
    'rest_framework'

]

MIDDLEWARE = [
    # 'django.middleware.cache.UpdateCacheMiddleware', #cache
    # 'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',#cache

]

ROOT_URLCONF = 'ePayment.urls'

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'cart.context_processors.cart'
            ],
        },
    },
]

WSGI_APPLICATION = 'ePayment.wsgi.application'



# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':     env('DB_NAME'),
        'USER':     env('DB_USER'),
        'PASSWORD': env('DB_PASS'),
        'HOST':     env('DB_HOST'),
        'PORT':     env('DB_PORT')
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE   = 'en-us'
TIME_ZONE       = 'Asia/Bangkok'
USE_I18N        = True
USE_L10N        = True
USE_TZ          = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/


STATIC_URL = '/static/'
# Local Static_root
# STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')
# Docker Static_root
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATIC_ROOT ='/staticfiles'


MEDIA_URL = '/media/'
# Docker Static_root
MEDIA_ROOT ='/media'



CART_SESSION_ID = 'cart'

CORS_ORIGIN_ALLOW_ALL=True
# CORS_ORIGIN_WHITELIST = (
#     "http://localhost:3000",
#     "http://127.0.0.1:3000"
# )

# Redirect the user to the home page after successful login
LOGIN_URL = '/auth/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'



# Added by Chutchai on Apr 26,2020 -- To support send Email function
DEFAULT_FROM_EMAIL = 'TestSite Team <noreply@example.com>'
EMAIL_RECIPIENT_LACKING_LIST = ['to1@example.com','to2@example.com']

# For email setting
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # During development only

# For Production setting
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SITE_ID = 1

CRISPY_TEMPLATE_PACK = 'bootstrap4'



# Debugging Tools
INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    'localhost'
    # ...
]

# QR_CODE_ENDPOINT_URL = env('QR_CODE_ENDPOINT_URL')
# EXPORT_BOOKING_ENDPOINT_URL = env('EXPORT_BOOKING_ENDPOINT_URL')
SLIP_VERIFY_ENDPOINT_URL = env('SLIP_VERIFY_ENDPOINT_URL')

# CACHES
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient"
#         },
#         "KEY_PREFIX": "default"
#     }
# }

# # Key in `CACHES` dict
# CACHE_MIDDLEWARE_ALIAS = 'default'
# # Additional prefix for cache keys
# CACHE_MIDDLEWARE_KEY_PREFIX = ''
# # Cache key TTL in seconds
# CACHE_MIDDLEWARE_SECONDS = 600

# Setup support for proxy headers
# USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_PROXY_SSL_HEADER = ('X-Forwarded-Proto', 'https')
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE =True
