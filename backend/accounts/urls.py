"""
Accounts 앱 - URL 설정
======================
사용자 인증 관련 URL 라우팅
"""

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # 회원가입
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # 로그인
    path('login/', views.CustomLoginView.as_view(), name='login'),
    
    # 로그아웃
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    
    # 프로필 조회
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
    
    # 프로필 수정
    path('profile/<str:username>/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
]
