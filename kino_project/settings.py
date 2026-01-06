import os
from pathlib import Path
import environ  # <--- WAŻNE: To musisz mieć zainstalowane (django-environ)

# Inicjalizacja zmiennych środowiskowych
env = environ.Env()
# Czytanie pliku .env (jeśli istnieje lokalnie)
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-n+zhd6fc(eg0w53x!2!8b_fu-+=4d%00^#6cohy$1(5wyth(_s'

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
    # Nasza aplikacja
    'main',
    # Aplikacje zewnętrzne
    'django_recaptcha',
    'django_otp',
    'django_otp.plugins.otp_totp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'kino_project.middleware.RemoveServerHeaderMiddleware',
]

ROOT_URLCONF = 'kino_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'kino_project.wsgi.application'

# --- KONFIGURACJA BAZY DANYCH (ZMIANA DLA CLOUD SQL) ---

# Pobieramy nazwę połączenia (ustawisz to w Cloud Run w sekcji Variables)
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')

if CLOUDSQL_CONNECTION_NAME:
    # Ustawienia dla Google Cloud Run (PostgreSQL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            # Kluczowe: połączenie przez Unix Socket w chmurze
            'HOST': f'/cloudsql/{CLOUDSQL_CONNECTION_NAME}',
            'PORT': '',
        }
    }
else:
    # Ustawienia lokalne (Twoje stare SQLite)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# -------------------------------------------------------

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'pl-PL'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = '/app/staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login/logout
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'main.backends.EmailOrUsernameBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Admin custom form
ADMIN_LOGIN_FORM = 'main.forms.AdminCaptchaForm'

# ReCaptcha keys
RECAPTCHA_PUBLIC_KEY = '6LctTyUsAAAAAOkR4x6JJeFHCMt8P7zqslL329UF'
RECAPTCHA_PRIVATE_KEY = '6LctTyUsAAAAAHrAeTf77du7kNMKkIGY5cIpdJwG'

# TOTP
OTP_TOTP_ISSUER = 'Moje Kino'

# Security headers
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
    'script-src': ("'self'", "'unsafe-inline'", 'cdn.jsdelivr.net', 'unpkg.com', 'cdnjs.cloudflare.com'),
    'style-src': ("'self'", "'unsafe-inline'", 'cdn.jsdelivr.net', 'fonts.googleapis.com'),
    'img-src': ("'self'", "data:", "https:"),
    'font-src': ("'self'", 'fonts.gstatic.com', 'cdn.jsdelivr.net'),
    'connect-src': ("'self'", 'tile.openstreetmap.org'),
}

# Session & CSRF cookies
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = False
