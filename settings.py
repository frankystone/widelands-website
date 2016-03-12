# Django settings for widelands project.

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+ '/widelands'
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dev.db',
        'USER': '',      # Not used with sqlite3.
        'PASSWORD': '',  # Not used with sqlite3.
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

SITE_ID = 1

# Where should logged in user go by default?
LOGIN_REDIRECT_URL = '/'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/wlmedia/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '#*bc7*q0-br42fc&6l^x@zzk&(=-#gr!)fn@t30n54n05jkqcu'

ROOT_URLCONF = 'urls'

#TEMPLATE_DIRS = () are now managed in TEMPLATES (Febr. 2016)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
#    'django.contrib.markup', # doesn't exist anymore
    'django.contrib.humanize',
    'threadedcomments',
    'django_comments',
    # Thirdparty apps, but need preload
#    'tracking',

    # Our own apps
    'wiki.templatetags.restructuredtext',
    'mainpage',
    'wlhelp',
    'wlimages',
    'wlwebchat',
    'wlrecaptcha',
    'wlprofile',
    'wlsearch',
    'wlpoll',
    'wlevents',
    'wlmaps',
    'wlscreens',
    'wlggz',

    # Modified 3rd party apps
    'wiki',  # This is based on wikiapp, but has some local modifications
    'news',  # This is based on simple-blog, but has some local modifications
    'news.managers',
    'pybb',  # Feature enriched version of pybb

    # Thirdparty apps
    'pinax.notifications', # Formerly notification, see next entry
    #'notification',
    'django_messages',
    'registration',  # User registration (per Email validation)
    'pagination',
    'tagging',
    #    'djangoratings', #No longer maintained
    #    'sphinxdoc',
    #    'south', Not longer supported
)

MIDDLEWARE_CLASSES = (
    # 'simplestats.middleware.RegexLoggingMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    # Remove this, when load gets to high or attachments are enabled
    'django.middleware.gzip.GZipMiddleware',
    'pagination.middleware.PaginationMiddleware',
    #    'tracking.middleware.VisitorTrackingMiddleware',
    #    'tracking.middleware.VisitorCleanUpMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django_messages.context_processors.inbox',
            ],
        },
    },
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'

#https://pypi.python.org/pypi/django-threadedcomments v 1.0.1
COMMENTS_APP = 'threadedcomments'

############################
# Activation configuration #
############################
DEFAULT_FROM_EMAIL = 'noreply@widelands.org'
ACCOUNT_ACTIVATION_DAYS = 2  # Days an activation token keeps active

######################
# Wiki configuration #
######################
WIKI_LOCK_DURATION = 30
WIKI_URL_RE = r'[:\-\w ]+'
WIKI_WORD_RE = r'[:\-\w ]+'

######################
# User configuration #
######################
#AUTH_PROFILE_MODULE = 'wlprofile.Profile' # NOCOMM: Must we change that? or use this at all?
# Don't use the following entry! It will affect the relationships from ManyToMany fields
#AUTH_USER_MODEL = 'wlprofile.Profile'

DEFAULT_TIME_ZONE = 3
DEFAULT_TIME_DISPLAY = r"%ND(Y-m-d,) H:i"  # According to ISO 8601
DEFAULT_MARKUP = 'markdown'
SIGNATURE_MAX_LENGTH = 255
SIGNATURE_MAX_LINES = 8
AVATARS_UPLOAD_TO = 'profile/avatars'
AVATAR_HEIGHT = AVATAR_WIDTH = 80

######################
# Pybb Configuration #
######################
PYBB_ATTACHMENT_ENABLE = False  # disable gzip middleware when enabling attachments
PYBB_DEFAULT_MARKUP = 'markdown'
PYBB_FREEZE_FIRST_POST = False

##############################################
# Link classification and other Markup stuff #
##############################################
LOCAL_DOMAINS = [
    'xoops.widelands.org'
]
SMILEY_DIR = MEDIA_URL + 'img/smileys/'
# Keep this list ordered by length of smileys
SMILEYS = [
    ('O:-)', 'face-angel.png'),
    ('O:)', 'face-angel.png'),
    (':-/', 'face-confused.png'),
    (':/', 'face-confused.png'),
    ('B-)', 'face-cool.png'),
    ('B)', 'face-cool.png'),
    (":'-(", 'face-crying.png'),
    (":'(", 'face-crying.png'),
    (':-))', 'face-smile-big.png'),
    (':))', 'face-smile-big.png'),
    (':-)', 'face-smile.png'),
    (':)', 'face-smile.png'),
    # Hack around markdown replacement. see also SMILEY_PREESCAPING
    ('&gt;:-)', 'face-devilish.png'),
    ('8-)', 'face-glasses.png'),
    ('8)', 'face-glasses.png'),
    (':-D', 'face-grin.png'),
    (':D', 'face-grin.png'),
    (':-x', 'face-kiss.png'),
    (':x', 'face-kiss.png'),
    (':-*', 'face-kiss.png'),
    (':*', 'face-kiss.png'),
    (':-((', 'face-mad.png'),
    (':((', 'face-mad.png'),
    (':-||', 'face-mad.png'),
    (':||', 'face-mad.png'),
    (':(|)', 'face-monkey.png'),
    (':-|', 'face-plain.png'),
    (':|', 'face-plain.png'),
    (':-(', 'face-sad.png'),
    (':(', 'face-sad.png'),
    (':-O', 'face-shock.png'),
    (':O', 'face-shock.png'),
    (':-o', 'face-surprise.png'),
    (':o', 'face-surprise.png'),
    (':-P', 'face-tongue.png'),
    (':P', 'face-tongue.png'),
    (':-S', 'face-upset.png'),
    (':S', 'face-upset.png'),
    (';-)', 'face-wink.png'),
    (';)', 'face-wink.png'),
]
# This needs to be done to keep some stuff hidden from markdown
SMILEY_PREESCAPING = [
    ('>:-)', '\>:-)')
]

###############################
# Sphinx (Search prog) Config #
###############################
USE_SPHINX = False
SPHINX_API_VERSION = 0x116

############
# Tracking #
############
TRACKING_CLEANUP_TIMEOUT = 48

###########################
# Widelands SVN directory #
###########################
# This is needed for various thinks, for example
# to access media (for minimap creation) or for online help
# or for ChangeLog displays
WIDELANDS_SVN_DIR = ''

#####################
# ChangeLog display #
#####################
BZR_URL = r"http://bazaar.launchpad.net/%%7Ewidelands-dev/widelands/trunk/revision/%s"

###############
# Screenshots #
###############
THUMBNAIL_SIZE = (160, 160)

########
# Maps #
########
MAPS_PER_PAGE = 10


USE_GOOGLE_ANALYTICS = False

##############################################
## Recipient(s) who get an email if someone ##
##       uses the on legal notice page      ##
## Use allways the form ('name', 'Email')   ##
##############################################
INQUIRY_RECIPIENTS = [
    ('peter', 'peter@example.com'),
]


try:
   from local_settings import *
except ImportError:
   pass

if USE_SPHINX:
   INSTALLED_APPS += (
       'djangosphinx',
   )
