"""
Blog 앱 - 필터
==============
DRF django-filter 필터 정의
게시글 검색 및 필터링
"""

import django_filters
from .models import Post, Comment


class PostFilter(django_filters.FilterSet):
    """
    게시글 필터
    
    필터 옵션:
    - title: 제목 검색 (부분 일치)
    - content: 내용 검색 (부분 일치)
    - search: 제목 또는 내용 검색
    - category: 카테고리 슬러그
    - author: 작성자 username
    - published: 발행 여부
    - created_after: 생성일 이후
    - created_before: 생성일 이전
    """
    
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        label='제목'
    )
    content = django_filters.CharFilter(
        lookup_expr='icontains',
        label='내용'
    )
    search = django_filters.CharFilter(
        method='filter_search',
        label='검색'
    )
    category = django_filters.CharFilter(
        field_name='category__slug',
        label='카테고리'
    )
    author = django_filters.CharFilter(
        field_name='author__username',
        label='작성자'
    )
    published = django_filters.BooleanFilter(
        label='발행'
    )
    created_after = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='생성일 이후'
    )
    created_before = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte',
        label='생성일 이전'
    )
    
    class Meta:
        model = Post
        fields = [
            'title', 'content', 'search',
            'category', 'author', 'published',
            'created_after', 'created_before'
        ]
    
    def filter_search(self, queryset, name, value):
        """제목 또는 내용에서 검색"""
        if value:
            return queryset.filter(
                django_filters.Q(title__icontains=value) |
                django_filters.Q(content__icontains=value)
            )
        return queryset


class CommentFilter(django_filters.FilterSet):
    """
    댓글 필터
    
    필터 옵션:
    - post: 게시글 ID
    - author: 작성자 username
    - is_active: 활성 상태
    """
    
    post = django_filters.NumberFilter(
        field_name='post__id',
        label='게시글'
    )
    author = django_filters.CharFilter(
        field_name='author__username',
        label='작성자'
    )
    is_active = django_filters.BooleanFilter(
        label='활성'
    )
    
    class Meta:
        model = Comment
        fields = ['post', 'author', 'is_active']
