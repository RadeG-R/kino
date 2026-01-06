import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-n+zhd6fc(eg0w53x!2!8b_fu-+=4d%00^#6cohy$1(5wyth(_s'
DEBUG = True
ALLOWED_HOSTS = ['*']

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
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pl-PL'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = [
    'main.backends.EmailOrUsernameBackend',
    'django.contrib.auth.backends.ModelBackend',
]

ADMIN_LOGIN_FORM = 'main.forms.AdminCaptchaForm'

RECAPTCHA_PUBLIC_KEY = '6LctTyUsAAAAAOkR4x6JJeFHCMt8P7zqslL329UF'
RECAPTCHA_PRIVATE_KEY = '6LctTyUsAAAAAHrAeTf77du7kNMKkIGY5cIpdJwG'

OTP_TOTP_ISSUER = 'Moje Kino'

SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
    'script-src': ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net", "unpkg.com", "cdnjs.cloudflare.com"),
    'style-src': ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net", "fonts.googleapis.com"),
    'img-src': ("'self'", "data:", "https:"),
    'font-src': ("'self'", "fonts.gstatic.com", "cdn.jsdelivr.net"),
    'connect-src': ("'self'", "tile.openstreetmap.org"),
}
X_CONTENT_TYPE_OPTIONS = 'nosniff'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = False
