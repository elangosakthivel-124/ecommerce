from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'
SECRET_KEY = os.getenv("SECRET_KEY")
'whitenoise.middleware.WhiteNoiseMiddleware',

DEBUG = os.getenv("DEBUG") == "True"
ALLOWED_HOSTS = ["*"]
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
web: gunicorn ecommerce.wsgi
python manage.py collectstatic
gunicorn ecommerce.wsgi
python manage.py createsuperuser
