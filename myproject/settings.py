"""
Django settings for the project.

This file is now configured to read all secrets (like SECRET_KEY
and database passwords) from environment variables, which are
provided by the .env file and docker-compose.yml.
"""
import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ---
# 1. CORE DJANGO & SECURITY (Reading from Docker Environment)
# ---

# SECRET_KEY is read from the .env file (via docker-compose)
SECRET_KEY = os.environ.get('SECRET_KEY')

# DEBUG is read from the .env file
# '1' == True, '0' == False
DEBUG = os.environ.get('DEBUG', '0') == '1'

# '*' is safe inside Docker, as only the container port is exposed.
ALLOWED_HOSTS = ['*']

# ---
# 2. APPLICATION DEFINITION
# ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # --- 3rd Party Apps ---
    'corsheaders',              # For React frontend
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',           # For admin filtering

    # --- Your Local Apps ---
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # --- CORS Middleware (must be high up) ---
    'corsheaders.middleware.CorsMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# This must match your project folder's name (e.g., 'myproject')
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

# This must also match your project folder's name (e.g., 'myproject')
WSGI_APPLICATION = 'myproject.wsgi.application'

# ---
# 3. DATABASE (Reading from Docker Environment)
# ---
# These values are provided by docker-compose.yml,
# which reads them from your .env file.
DB_NAME = os.environ.get('POSTGRES_DB')
DB_USER = os.environ.get('POSTGRES_USER')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DB_HOST = os.environ.get('POSTGRES_HOST') # This will be 'db'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': '5432', # Default Postgres port
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
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ---
# 4. Static files (CSS, JavaScript, Images) -- THIS IS THE FIX
# https://docs.djangoproject.com/en/5.0/howto/static-files/
# ---

# This is the URL path where static files will be served from (e.g., /static/style.css)
STATIC_URL = '/static/'
# This is the directory where 'collectstatic' will gather all static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (user-uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ---
# 5. REST FRAMEWORK & JWT SETTINGS (for HttpOnly Cookies)
# ---

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # Use our new custom cookie authenticator
        'api.authentication.CookieJWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # Default to requiring login
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        # Enable filtering globally
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    
    # Use our custom serializers to handle cookies and user data
    'TOKEN_OBTAIN_SERIALIZER': 'api.serializers.CustomTokenObtainPairSerializer',
    'TOKEN_REFRESH_SERIALIZER': 'api.serializers.CustomTokenRefreshSerializer',

    # Name of the cookie to look for
    'ACCESS_TOKEN_COOKIE': 'access_token',
}

# ---
# 6. CORS & COOKIE SECURITY SETTINGS
# ---

# This allows your React app (at http://localhost:3000)
# to make requests to this backend.
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5500",
    "http://192.168.8.85:8081",
]
# This is CRITICAL. It allows the browser to send
# your HttpOnly cookies to the backend.
CORS_ALLOW_CREDENTIALS = True

# For http://localhost development, these MUST be False
# or the browser will reject the cookies.
CSRF_COOKIE_SECURE = False 
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'

# ---
# 7. CUSTOM APP SETTINGS (Reading from Docker Environment)
# ---

# Your secret key for the bus scanner API
BUS_API_KEY = os.environ.get('BUS_API_KEY')