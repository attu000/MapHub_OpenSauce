import os
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# django-environの初期化
env = environ.Env(
    # 環境変数が存在しない場合のデフォルト値と型を定義
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, [])
)

# .env ファイルが存在する場合（ローカル環境など）は読み込む
# 本番環境でサーバーの環境変数として設定されている場合はそこから読み込まれます
env_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(env_file):
    env.read_env(env_file)

# ==========================================
# セキュリティ・環境変数設定
# ==========================================
# SECRET_KEYは.envから取得する
SECRET_KEY = env('SECRET_KEY')

# DEBUGモードも.envから取得する
DEBUG = env('DEBUG')

# ALLOWED_HOSTSも.envから取得する（カンマ区切りでリスト化されます）
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


# ==========================================
# アプリケーション定義
# ==========================================
INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',
    'mymapapp.apps.MymapappConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'mymap.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # プロジェクトルートのtemplatesを追加
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

WSGI_APPLICATION = 'mymap.wsgi.application'


# ==========================================
# データベース設定
# ==========================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ==========================================
# パスワードバリデーション・国際化
# ==========================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'ja'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ==========================================
# 静的ファイル (CSS, JavaScript, Images)
# ==========================================
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'mymapapp/static'),
]
#本番環境（DEBUG=False）で静的ファイルを集約・配信するためのディレクトリ設定
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# ==========================================
# メディアファイル (ユーザーアップロード画像)
# ==========================================
MEDIA_URL = '/media/'
#PythonAnywhereの構造に合わせた安全なパス設定に統一
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ==========================================
# 認証・カスタムユーザー設定
# ==========================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.CustomUser'
LOGIN_URL = "accounts:login"


LOGIN_REDIRECT_URL = "mymapapp:site_list"


# ==========================================
# 本番環境向けの動的セキュリティ設定
# ==========================================
# DEBUG=False（本番環境）の時のみ、セキュリティCookie等の設定を自動でTrueにする
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG