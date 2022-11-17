from pathlib import Path
from django.contrib.messages import constants
from django.urls import reverse_lazy

import os
import sys


BASE_DIR = Path(__file__).resolve().parent.parent



# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)(moemh8_vhe3=1n6xs9m2$ltxkq)$_%nadd^1#&gy)zg8#yw7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# usar a pasta templates como pasta que faz parte do projeto
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')


# usar a pasta apps como pasta que faz parte do projeto
sys.path.append(os.path.join(BASE_DIR, 'apps'))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS += [
    'core',
    'products',
    'cart',
    'inventory',
    'sales_products',
    'users',
    'management',
    
    'django_forms_bootstrap',
    'bootstrap_datepicker_plus'
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

ROOT_URLCONF = 'gestao_vendas.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'gestao_vendas.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ddom7i4fkvi8s2',
        'USER': 'rskpyogedkwgua',
        'PASSWORD': 'a567966724afe1728c2e2d0a32251483958c7e98fbb930d8f7b4dbef2adba254',
        'HOST': 'ec2-3-219-135-162.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

'''
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True



# ESTATICOS DO PROJETO
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# para poder usar arquivsos de media 
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = "/media/"

# Após fazer o login , redirecionar para a pagina home
#LOGIN_REDIRECT_URL  = 'home'

LOGOUT_REDIRECT_URL = reverse_lazy('login')
LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('login')

MESSAGE_TAGS = {
constants.DEBUG: '-primary',
constants.ERROR: '-danger',
constants.SUCCESS: '-success',
constants.INFO: '-info',
constants.WARNING: '-warning'
}


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
