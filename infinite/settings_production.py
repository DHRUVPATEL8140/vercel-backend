"""
Production settings for infinite project.
"""

from .settings import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-6em9se)6$0*$eg-mwyrcl3gwz@b@zl9r0)r3!86@_cu8p&rsl+')

# Database
# Use environment variables for production database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'infinite_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-domain.vercel.app",
    "https://your-frontend-domain.netlify.app",
]

# CSRF settings
CSRF_TRUSTED_ORIGINS = [
    "https://your-frontend-domain.vercel.app",
    "https://your-frontend-domain.netlify.app",
]

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Remove MongoDB configuration for production
DATABASES.pop('mongo', None)
