"""
Accounts 앱 - 관리자 설정
========================
Django Admin에서 사용자 모델 관리
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    커스텀 사용자 관리자
    
    기능:
    - 사용자 목록 표시 (이메일, 가입일 등)
    - 사용자 상세 정보 편집
    - 프로필 이미지 미리보기
    """
    
    # 목록 페이지 설정
    list_display = (
        'username', 'email', 'get_full_name', 
        'is_active', 'is_staff', 'date_joined'
    )
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'email_verified')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    # 상세 페이지 필드셋
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('개인 정보'), {
            'fields': ('first_name', 'last_name', 'email', 'profile_image', 'bio')
        }),
        (_('권한'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'email_verified', 'groups', 'user_permissions'),
        }),
        (_('중요 날짜'), {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    # 사용자 추가 페이지 필드셋
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
    # 읽기 전용 필드
    readonly_fields = ('date_joined', 'last_login')
