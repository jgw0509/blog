"""
Accounts 앱 - 사용자 모델
========================
커스텀 사용자 모델 정의
Django의 AbstractUser를 확장하여 추가 필드 제공

모델 구조:
- User: 커스텀 사용자 모델 (이메일, 프로필 이미지, 자기소개)
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    커스텀 사용자 모델
    
    기본 필드 (AbstractUser에서 상속):
    - username: 사용자명
    - email: 이메일
    - password: 비밀번호
    - first_name: 이름
    - last_name: 성
    - is_active: 활성화 여부
    - is_staff: 스태프 여부
    - is_superuser: 슈퍼유저 여부
    - date_joined: 가입일
    - last_login: 마지막 로그인
    
    추가 필드:
    - profile_image: 프로필 이미지
    - bio: 자기소개
    """
    
    # 이메일 필드를 필수로 변경
    email = models.EmailField(
        _('이메일 주소'),
        unique=True,
        error_messages={
            'unique': _('이미 사용 중인 이메일 주소입니다.'),
        },
    )
    
    # 프로필 이미지
    profile_image = models.ImageField(
        _('프로필 이미지'),
        upload_to='profiles/%Y/%m/',
        blank=True,
        null=True,
        help_text=_('프로필 이미지를 업로드하세요.')
    )
    
    # 자기소개
    bio = models.TextField(
        _('자기소개'),
        max_length=500,
        blank=True,
        help_text=_('500자 이내로 자신을 소개해주세요.')
    )
    
    # 이메일 인증 여부
    email_verified = models.BooleanField(
        _('이메일 인증'),
        default=False,
        help_text=_('이메일 인증 완료 여부')
    )
    
    class Meta:
        verbose_name = _('사용자')
        verbose_name_plural = _('사용자 목록')
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        """전체 이름 반환 (한국식: 성+이름)"""
        full_name = f'{self.last_name}{self.first_name}'
        return full_name.strip() or self.username
    
    def get_post_count(self):
        """작성한 게시글 수 반환"""
        return self.posts.count()
    
    def get_comment_count(self):
        """작성한 댓글 수 반환"""
        return self.comments.count()
