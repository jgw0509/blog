"""
Django 블로그 프로젝트 설정 파일
================================
환경변수 기반 설정으로 개발/운영 환경 분리
보안 설정 및 최적화 적용

설정 구조:
- 기본 설정 (BASE_DIR, SECRET_KEY 등)
- 앱 설정 (INSTALLED_APPS)
- 미들웨어 설정
- 데이터베이스 설정 (PostgreSQL)
- 인증 설정
- 정적 파일 설정
- REST Framework 설정
- 보안 설정
"""

import os
from pathlib import Path
from decouple import config, Csv

# ===========================================
# 기본 설정
# ===========================================

# 프로젝트 루트 디렉토리
BASE_DIR = Path(__file__).resolve().parent.parent

# 보안 경고: 운영 환경에서는 반드시 환경변수로 설정!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-in-production')

# 디버그 모드 (운영 환경에서는 반드시 False)
DEBUG = config('DEBUG', default=False, cast=bool)

# 허용 호스트
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# ===========================================
# 앱 설정
# ===========================================

INSTALLED_APPS = [
    # Django 기본 앱
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 서드파티 앱
    'rest_framework',           # Django REST Framework
    'rest_framework.authtoken', # Token 인증
    'django_filters',           # API 필터링
    'corsheaders',             # CORS 지원
    
    # 프로젝트 앱
    'accounts.apps.AccountsConfig',  # 사용자 인증
    'blog.apps.BlogConfig',          # 블로그 핵심 기능
    'api.apps.ApiConfig',            # REST API
    
    # 에디터
    'django_summernote',
]

# ===========================================
# 미들웨어 설정
# ===========================================

MIDDLEWARE = [
    # 보안 미들웨어 (가장 먼저 실행)
    'django.middleware.security.SecurityMiddleware',
    # 정적 파일 서빙 (whitenoise)
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # CORS 미들웨어
    'corsheaders.middleware.CorsMiddleware',
    # 세션 미들웨어
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 공통 미들웨어
    'django.middleware.common.CommonMiddleware',
    # CSRF 보호
    'django.middleware.csrf.CsrfViewMiddleware',
    # 인증 미들웨어
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 메시지 미들웨어
    'django.contrib.messages.middleware.MessageMiddleware',
    # 클릭재킹 방지
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ===========================================
# URL 및 템플릿 설정
# ===========================================

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # 프로젝트 레벨 템플릿
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

WSGI_APPLICATION = 'config.wsgi.application'

# ===========================================
# 데이터베이스 설정 (PostgreSQL)
# ===========================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB', default='blog_db'),
        'USER': config('POSTGRES_USER', default='blog_user'),
        'PASSWORD': config('POSTGRES_PASSWORD', default='blog_password'),
        'HOST': config('POSTGRES_HOST', default='localhost'),
        'PORT': config('POSTGRES_PORT', default='5432'),
        # 연결 최적화
        'CONN_MAX_AGE': 60,  # 연결 재사용 (초)
        'OPTIONS': {
            'connect_timeout': 10,
        },
    }
}

# ===========================================
# 커스텀 사용자 모델
# ===========================================

AUTH_USER_MODEL = 'accounts.User'

# ===========================================
# 비밀번호 검증
# ===========================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ===========================================
# 국제화 설정
# ===========================================

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

# ===========================================
# 정적 파일 설정
# ===========================================

# URL 경로
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# 파일 시스템 경로
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'

# 개발용 정적 파일 디렉토리
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# WhiteNoise 정적 파일 압축
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ===========================================
# 기본 Primary Key 설정
# ===========================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ===========================================
# Django REST Framework 설정
# ===========================================

REST_FRAMEWORK = {
    # 기본 인증 클래스
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    # 기본 권한 클래스
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    # 페이지네이션
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    # 필터링
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    # 스로틀링 (API 요청 제한)
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',     # 비인증 사용자
        'user': '1000/hour',    # 인증 사용자
    },
}

# ===========================================
# CORS 설정
# ===========================================

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOWED_ORIGINS = config(
        'CORS_ALLOWED_ORIGINS',
        default='http://localhost:3000',
        cast=Csv()
    )

# ===========================================
# 보안 설정 (운영 환경)
# ===========================================

if not DEBUG:
    # HTTPS 강제
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # HSTS 설정
    SECURE_HSTS_SECONDS = 31536000  # 1년
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # XSS 필터
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    
    # X-Frame-Options
    X_FRAME_OPTIONS = 'DENY'

# Summernote 설정
SUMMERNOTE_CONFIG = {
    'iframe': True,
    'summernote': {
        'width': '100%',
        'height': '400',
        'lang': 'ko-KR',  # 한국어 설정
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'italic', 'underline', 'clear']],
            ['fontname', ['fontname']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['table', ['table']],
            ['insert', ['link', 'picture', 'video']],
            ['view', ['fullscreen', 'codeview', 'help']],
        ],
    },
}

X_FRAME_OPTIONS = 'SAMEORIGIN'

# ===========================================
# 로깅 설정
# ===========================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': config('DJANGO_LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
    },
}

# ===========================================
# 로그인 URL 설정
# ===========================================

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
