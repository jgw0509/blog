"""
API 앱 - URL 설정
=================
DRF Router 기반 URL 라우팅
REST API 엔드포인트 정의
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

# DRF Router 설정
router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'comments', views.CommentViewSet, basename='comment')
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    # Router URL
    path('', include(router.urls)),
    
    # 인증 API
    path('auth/register/', views.RegisterAPIView.as_view(), name='register'),
    path('auth/login/', views.LoginAPIView.as_view(), name='login'),
    path('auth/logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('auth/password-change/', views.PasswordChangeAPIView.as_view(), name='password-change'),
    path('auth/me/', views.CurrentUserAPIView.as_view(), name='current-user'),
    
    # 게시글 댓글 API
    path('posts/<slug:slug>/comments/', views.PostCommentAPIView.as_view(), name='post-comments'),
]

"""
API 엔드포인트 목록
==================

인증:
  POST   /api/auth/register/         - 회원가입
  POST   /api/auth/login/            - 로그인
  POST   /api/auth/logout/           - 로그아웃
  POST   /api/auth/password-change/  - 비밀번호 변경
  GET    /api/auth/me/               - 현재 사용자

카테고리:
  GET    /api/categories/            - 목록
  POST   /api/categories/            - 생성
  GET    /api/categories/{slug}/     - 상세
  PUT    /api/categories/{slug}/     - 수정
  DELETE /api/categories/{slug}/     - 삭제

게시글:
  GET    /api/posts/                 - 목록 (검색: ?search=, ?category=)
  POST   /api/posts/                 - 생성
  GET    /api/posts/{slug}/          - 상세
  PUT    /api/posts/{slug}/          - 수정
  DELETE /api/posts/{slug}/          - 삭제
  POST   /api/posts/{slug}/increase_view/ - 조회수 증가

댓글:
  GET    /api/posts/{slug}/comments/ - 게시글 댓글 목록
  POST   /api/posts/{slug}/comments/ - 댓글 작성
  GET    /api/comments/              - 전체 댓글 목록
  PUT    /api/comments/{id}/         - 댓글 수정
  DELETE /api/comments/{id}/         - 댓글 삭제

사용자:
  GET    /api/users/                 - 목록
  GET    /api/users/{username}/      - 상세
"""
