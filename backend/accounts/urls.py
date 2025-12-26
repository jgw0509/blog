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
    
    # ==================== 팔로우 관련 URL ====================
    path('profile/<str:username>/follow/', views.toggle_follow, name='toggle_follow'),
    path('profile/<str:username>/followers/', views.follower_list, name='follower_list'),
    path('profile/<str:username>/following/', views.following_list, name='following_list'),
    
    # ==================== 알림 관련 URL ====================
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/read-all/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('notifications/<int:pk>/delete/', views.delete_notification, name='delete_notification'),
]

