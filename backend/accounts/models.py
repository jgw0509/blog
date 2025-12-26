"""
Accounts 앱 - 사용자 모델
========================
커스텀 사용자 모델 정의
Django의 AbstractUser를 확장하여 추가 필드 제공

모델 구조:
- User: 커스텀 사용자 모델 (이메일, 프로필 이미지, 자기소개)
- Follow: 팔로우 관계 모델
- Notification: 알림 모델
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
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
    
    def get_follower_count(self):
        """팔로워 수 반환"""
        return self.followers.count()
    
    def get_following_count(self):
        """팔로잉 수 반환"""
        return self.following.count()
    
    def is_following(self, user):
        """특정 사용자를 팔로우 중인지 확인"""
        return self.following.filter(following=user).exists()
    
    def get_unread_notification_count(self):
        """읽지 않은 알림 수 반환"""
        return self.notifications.filter(is_read=False).count()


class Follow(models.Model):
    """
    팔로우 관계 모델
    
    사용자 간 팔로우/팔로잉 관계를 저장
    
    필드:
    - follower: 팔로우 하는 사용자
    - following: 팔로우 받는 사용자
    - created_at: 팔로우 시작일
    """
    
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='팔로워'
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='팔로잉'
    )
    created_at = models.DateTimeField(
        '팔로우 시작일',
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = '팔로우'
        verbose_name_plural = '팔로우 목록'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'following'],
                name='unique_follow'
            )
        ]
    
    def __str__(self):
        return f'{self.follower.username} → {self.following.username}'


class Notification(models.Model):
    """
    알림 모델
    
    사용자에게 전달되는 알림
    
    필드:
    - recipient: 알림 받는 사용자
    - sender: 알림 발생시킨 사용자
    - notification_type: 알림 종류
    - post: 관련 게시글 (Optional)
    - comment: 관련 댓글 (Optional)
    - message: 알림 메시지
    - is_read: 읽음 여부
    - created_at: 생성일
    """
    
    NOTIFICATION_TYPES = [
        ('comment', '댓글'),
        ('reply', '대댓글'),
        ('like', '좋아요'),
        ('follow', '팔로우'),
        ('new_post', '새 게시글'),
    ]
    
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='수신자'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_notifications',
        verbose_name='발신자'
    )
    notification_type = models.CharField(
        '알림 종류',
        max_length=20,
        choices=NOTIFICATION_TYPES
    )
    post = models.ForeignKey(
        'blog.Post',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications',
        verbose_name='게시글'
    )
    comment = models.ForeignKey(
        'blog.Comment',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications',
        verbose_name='댓글'
    )
    message = models.CharField(
        '알림 메시지',
        max_length=255
    )
    is_read = models.BooleanField(
        '읽음',
        default=False
    )
    created_at = models.DateTimeField(
        '생성일',
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = '알림'
        verbose_name_plural = '알림 목록'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.recipient.username}: {self.message[:30]}'
    
    def mark_as_read(self):
        """알림을 읽음으로 표시"""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])

