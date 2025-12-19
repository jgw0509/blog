"""
Blog 앱 - 모델
==============
블로그 핵심 모델 정의
게시글, 댓글, 카테고리 모델

모델 구조:
- Category: 게시글 카테고리
- Post: 게시글 (제목, 내용, 작성자, 카테고리 등)
- Comment: 댓글 (게시글, 작성자, 내용)
- Bookmark: 북마크 (사용자, 게시글)
"""

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings


class Category(models.Model):
    """
    카테고리 모델
    
    게시글 분류를 위한 카테고리
    계층 구조는 지원하지 않음 (단일 레벨)
    
    필드:
    - name: 카테고리 이름
    - slug: URL 친화적 식별자
    - description: 카테고리 설명
    - created_at: 생성일
    """
    
    name = models.CharField(
        '카테고리명',
        max_length=100,
        unique=True
    )
    slug = models.SlugField(
        '슬러그',
        max_length=100,
        unique=True,
        allow_unicode=True,  # 한글 슬러그 허용
        help_text='URL에 사용될 식별자 (자동 생성)'
    )
    description = models.TextField(
        '설명',
        blank=True,
        help_text='카테고리에 대한 간단한 설명'
    )
    created_at = models.DateTimeField(
        '생성일',
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리 목록'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """슬러그 자동 생성"""
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:category_detail', kwargs={'slug': self.slug})
    
    def get_post_count(self):
        """카테고리 내 게시글 수"""
        return self.posts.filter(published=True).count()


class Post(models.Model):
    """
    게시글 모델
    
    블로그의 핵심 콘텐츠
    
    필드:
    - title: 제목
    - slug: URL 친화적 식별자
    - content: 본문 내용
    - author: 작성자 (User FK)
    - category: 카테고리 (Category FK)
    - thumbnail: 썸네일 이미지
    - published: 발행 여부
    - created_at: 생성일
    - updated_at: 수정일
    - views: 조회수
    """
    
    title = models.CharField(
        '제목',
        max_length=200
    )
    slug = models.SlugField(
        '슬러그',
        max_length=200,
        unique=True,
        allow_unicode=True,
        help_text='URL에 사용될 식별자'
    )
    content = models.TextField(
        '내용'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='작성자'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='카테고리'
    )
    thumbnail = models.ImageField(
        '썸네일',
        upload_to='posts/thumbnails/%Y/%m/',
        blank=True,
        null=True,
        help_text='게시글 썸네일 이미지'
    )
    published = models.BooleanField(
        '발행',
        default=True,
        help_text='체크 해제 시 비공개 상태'
    )
    created_at = models.DateTimeField(
        '생성일',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        '수정일',
        auto_now=True
    )
    views = models.PositiveIntegerField(
        '조회수',
        default=0
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_posts',
        blank=True,
        verbose_name='좋아요'
    )
    dislikes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='disliked_posts',
        blank=True,
        verbose_name='싫어요'
    )
    
    class Meta:
        verbose_name = '게시글'
        verbose_name_plural = '게시글 목록'
        ordering = ['-created_at']
        # 조회 최적화를 위한 인덱스
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['author', '-created_at']),
            models.Index(fields=['category', '-created_at']),
            models.Index(fields=['published', '-created_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """슬러그 자동 생성 (제목 + 타임스탬프)"""
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)
            # 유니크 슬러그 생성
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            self.slug = f'{base_slug}-{timestamp}'
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    def get_comment_count(self):
        """댓글 수 반환"""
        return self.comments.count()
    
    def increase_views(self):
        """조회수 증가"""
        self.views += 1
        self.save(update_fields=['views'])
    
    def get_related_posts(self, limit=5):
        """관련 게시글 (같은 카테고리)"""
        if self.category:
            return Post.objects.filter(
                category=self.category,
                published=True
            ).exclude(pk=self.pk).order_by('-created_at')[:limit]
        return Post.objects.none()


class Comment(models.Model):
    """
    댓글 모델
    
    게시글에 달린 댓글
    대댓글(답글) 기능 포함
    
    필드:
    - post: 게시글 (Post FK)
    - author: 작성자 (User FK)
    - parent: 부모 댓글 (대댓글용)
    - content: 댓글 내용
    - created_at: 생성일
    - updated_at: 수정일
    - is_active: 활성 상태 (삭제 시 False)
    """
    
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='게시글'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='작성자'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='부모 댓글'
    )
    content = models.TextField(
        '내용',
        max_length=1000
    )
    created_at = models.DateTimeField(
        '생성일',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        '수정일',
        auto_now=True
    )
    is_active = models.BooleanField(
        '활성',
        default=True,
        help_text='삭제된 댓글은 비활성 상태'
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_comments',
        blank=True,
        verbose_name='좋아요'
    )
    dislikes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='disliked_comments',
        blank=True,
        verbose_name='싫어요'
    )
    
    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'
        ordering = ['created_at']
    
    def __str__(self):
        return f'{self.author.username}: {self.content[:30]}'
    
    def get_replies(self):
        """대댓글 목록"""
        return self.replies.filter(is_active=True)
    
    @property
    def is_parent(self):
        """부모 댓글인지 확인"""
        return self.parent is None


class Bookmark(models.Model):
    """
    북마크 모델
    
    사용자가 저장한 게시글
    UniqueTogether 제약으로 중복 저장 방지
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookmarks',
        verbose_name='사용자'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='bookmarks',
        verbose_name='게시글'
    )
    created_at = models.DateTimeField(
        '저장일',
        auto_now_add=True
    )

    class Meta:
        verbose_name = '북마크'
        verbose_name_plural = '북마크 목록'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'],
                name='unique_user_post_bookmark'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.post.title}'
