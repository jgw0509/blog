"""
Blog 앱 - 관리자 설정
====================
Django Admin에서 게시글, 댓글, 카테고리 관리
"""

from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    카테고리 관리자
    
    기능:
    - 카테고리 목록 표시
    - 슬러그 자동 생성
    - 게시글 수 표시
    """
    
    list_display = ('name', 'slug', 'get_post_count', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    
    def get_post_count(self, obj):
        return obj.get_post_count()
    get_post_count.short_description = '게시글 수'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    게시글 관리자
    
    기능:
    - 게시글 목록 (제목, 작성자, 카테고리, 발행 상태)
    - 썸네일 미리보기
    - 일괄 발행/비공개 처리
    - 필터링 및 검색
    """
    
    list_display = (
        'title', 'author', 'category', 
        'published', 'views', 'created_at', 'thumbnail_preview'
    )
    list_filter = ('published', 'category', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    # 성능 최적화: 관련 객체 미리 로드
    list_select_related = ('author', 'category')
    
    # 상세 페이지 필드셋
    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('내용', {
            'fields': ('content', 'thumbnail')
        }),
        ('발행 설정', {
            'fields': ('published',)
        }),
        ('통계', {
            'fields': ('views',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('views',)
    
    def thumbnail_preview(self, obj):
        """썸네일 미리보기"""
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover;" />',
                obj.thumbnail.url
            )
        return '-'
    thumbnail_preview.short_description = '썸네일'
    
    actions = ['make_published', 'make_unpublished']
    
    @admin.action(description='선택한 게시글 발행')
    def make_published(self, request, queryset):
        count = queryset.update(published=True)
        self.message_user(request, f'{count}개의 게시글이 발행되었습니다.')
    
    @admin.action(description='선택한 게시글 비공개')
    def make_unpublished(self, request, queryset):
        count = queryset.update(published=False)
        self.message_user(request, f'{count}개의 게시글이 비공개되었습니다.')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    댓글 관리자
    
    기능:
    - 댓글 목록 (게시글, 작성자, 내용 미리보기)
    - 활성/비활성 상태 관리
    - 일괄 삭제(비활성화) 처리
    """
    
    list_display = (
        'get_post_title', 'author', 'content_preview',
        'is_active', 'is_reply', 'created_at'
    )
    list_filter = ('is_active', 'created_at')
    search_fields = ('content', 'author__username', 'post__title')
    ordering = ('-created_at',)
    
    # 성능 최적화
    list_select_related = ('post', 'author', 'parent')
    
    def get_post_title(self, obj):
        return obj.post.title[:30]
    get_post_title.short_description = '게시글'
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = '내용'
    
    def is_reply(self, obj):
        return obj.parent is not None
    is_reply.boolean = True
    is_reply.short_description = '답글'
    
    actions = ['activate_comments', 'deactivate_comments']
    
    @admin.action(description='선택한 댓글 활성화')
    def activate_comments(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count}개의 댓글이 활성화되었습니다.')
    
    @admin.action(description='선택한 댓글 비활성화 (삭제)')
    def deactivate_comments(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count}개의 댓글이 비활성화되었습니다.')
