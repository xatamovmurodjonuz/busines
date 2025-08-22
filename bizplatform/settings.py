import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'YOUR_SECRET_KEY_HERE'  # Bu o‘zingiz uchun maxfiy qilib qo‘ying

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'mainapp',  # Bizning app

    'django.contrib.sites',  # allauth uchun
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'rest_framework',  # keyinchalik API uchun
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'bizplatform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # umumiy template papkasi
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # allauth uchun
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bizplatform.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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


LANGUAGE_CODE = 'uz'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Login va logoutdan keyin yo'naltirish
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Allauth sozlamalari
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # default
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'
