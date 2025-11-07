from pathlib import Path
import os
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-n--j@56e_to4ys5ywhtsffuw2f4#ei*3lnv13sw#fm75f$iyto'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'carrito',
    'rest_framework',
    'useradmin.apps.UseradminConfig',    # asegurar que use AppConfig
    'django_api',
    'rest_framework_simplejwt',
    'corsheaders',
]

AUTH_USER_MODEL = 'useradmin.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),     # Token de acceso (para las peticiones)
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),        # Token de refresco (para obtener nuevos tokens)
    'ROTATE_REFRESH_TOKENS': True, # Rotar token de refresco por seguridad
    'AUTH_HEADER_TYPES': ('Bearer',), # Formato del header: Authorization: Bearer <token>
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',            # <- PRIMERO
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',        # <- siempre debajo de CorsMiddleware
    #'django.middleware.csrf.CsrfViewMiddleware', 
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_api.urls'

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

WSGI_APPLICATION = 'django_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

import pymysql
pymysql.install_as_MySQLdb()

# --- COMIENZA LA MODIFICACIÓN: soporta entorno Railway (producción) y local (desarrollo) ---
# Detectar si estamos en un entorno de Railway (u otro PaaS) mediante una variable de entorno
IS_RAILWAY_ENV = os.environ.get('RAILWAY_ENVIRONMENT') is not None or os.environ.get('RAILWAY_DATABASE_URL') is not None

if IS_RAILWAY_ENV:
    # 🚨 CONFIGURACIÓN DE PRODUCCIÓN (Railway / MySQL)
    # Railway (u otros PaaS) normalmente inyecta credenciales en variables de entorno.
    # Asegurate en Railway de definir: MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # SOLO BUSCA las variables estándar de MySQL
        'NAME': os.environ.get('MYSQL_DATABASE'), 
        'USER': os.environ.get('MYSQL_USER'),      
        'PASSWORD': os.environ.get('MYSQL_PASSWORD'), 
        'HOST': os.environ.get('MYSQL_HOST'),      
        'PORT': os.environ.get('MYSQL_PORT', '3306'), # Si no lo encuentra, usa 3306
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
    # Recomendación de seguridad en producción
    DEBUG = False
    ALLOWED_HOSTS = ['*']
else:
    # 💻 CONFIGURACIÓN DE DESARROLLO (Localhost)
    DATABASES = { 
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'todosport', 
            'USER': 'root', 
            'PASSWORD': '1234',
            'HOST': 'localhost',
            'PORT': '3306',
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
    DEBUG = True
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# --- FIN DE LA MODIFICACIÓN ---


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 🛠️ AJUSTE DE CONFIANZA DEL PROXY (CLAVE PARA RAILWAY/NETLIFY)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
# -----------------------------------------------------------

CORS_ALLOW_ALL_ORIGINS = False # Se recomienda no usar True en producción
CORS_ALLOWED_ORIGINS: list[str] = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'https://todosportgaston.netlify.app',
]

# 🛠️ FORZAR SEGURIDAD HTTPS Y CSRF
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True # Esto fuerza HTTPS, aunque Railway lo maneja

# Si tu Django es 4.x y usás cookies en algún endpoint, agrega:
CSRF_TRUSTED_ORIGINS: list[str] = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'https://todosportgaston.netlify.app',
]

# Para depurar, podés habilitar temporalmente:
# CORS_ALLOW_ALL_ORIGINS = True

# settings.py (Añadir o modificar al final del archivo)

# 26214400 bytes = 25 MB
# Aumenta el límite de memoria para datos POST:
DATA_UPLOAD_MAX_MEMORY_SIZE = 26214400 

# Aumenta el límite del tamaño máximo de archivos subidos (necesario para POST/PUT)
FILE_UPLOAD_MAX_MEMORY_SIZE = 26214400