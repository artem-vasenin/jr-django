from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # Используем базу в памяти
    }
}

MIDDLEWARE = [mw for mw in MIDDLEWARE if mw not in [
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]]

DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
