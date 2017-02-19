import environ
from django.contrib.messages import constants as message_constants

root = environ.Path(__file__) - 3 # three folder back (/a/b/c/ - 3 = /)
env  = environ.Env(DEBUG=(bool, False),) # set default values and casting
environ.Env.read_env() # reading .env file

SITE_ROOT = root()
DEBUG     = env('DEBUG')
DATABASES = {
  'default': env.db(),
  'extra': env.db('SQLITE_URL', default='sqlite:////tmp/my-tmp-sqlite.db')
}

if not DEBUG:
  ALLOWED_HOSTS = ['.herokuapp.com']


SECRET_KEY       = env('SECRET_KEY') # Raises ImproperlyConfigured exception if SECRET_KEY not in os.environ
public_root      = root.path('/')
STATIC_ROOT      = public_root('static')
STATIC_URL       = '/static/'
STATICFILES_DIRS = (SITE_ROOT, 'static')

INSTALLED_APPS = [
  'home.apps.HomeConfig',
  'accounts.apps.AccountsConfig',
  'envelopes.apps.EnvelopesConfig',
  'transactions.apps.TransactionsConfig',
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'money.urls'

TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
      'debug': DEBUG,
      'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
      ],
    },
  },
]

WSGI_APPLICATION = 'money.wsgi.application'

MESSAGE_TAGS = {
  message_constants.INFO: 'bg--blue fnt--off-white p1',
  message_constants.SUCCESS: 'bg--green fnt--off-white p1',
  message_constants.WARNING: 'bg--orange p1',
  message_constants.ERROR: 'bg--red fnt--off-white p1',
}

AUTH_PASSWORD_VALIDATORS = [
  {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
  {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
  {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
  {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_URL          = '/login/'
LOGIN_REDIRECT_URL = '/home'
LANGUAGE_CODE      = 'en-nz'
TIME_ZONE          = 'Europe/London'
USE_I18N           = True
USE_L10N           = True
USE_TZ             = True
