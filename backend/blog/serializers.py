"""
Blog 앱 - 시리얼라이저
======================
DRF 시리얼라이저 정의
REST API를 통한 블로그 데이터 직렬화
"""

from rest_framework import serializers
from .models import Category, Post, Comment
from accounts.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    """
    카테고리 시리얼라이저
    
    게시글 수 포함
    """
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'post_count', 'created_at']
        read_only_fields = ['id', 'slug', 'created_at']
    
    def get_post_count(self, obj):
        return obj.get_post_count()


class CommentSerializer(serializers.ModelSerializer):
    """
    댓글 시리얼라이저
    
    작성자 정보 중첩
    대댓글 지원
    """
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'author', 'content', 'parent',
            'created_at', 'updated_at', 'is_active', 'replies'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def get_replies(self, obj):
        """대댓글 목록"""
        if obj.parent is None:  # 부모 댓글인 경우만
            replies = obj.replies.filter(is_active=True)
            return CommentSerializer(replies, many=True).data
        return []


class CommentCreateSerializer(serializers.ModelSerializer):
    """
    댓글 생성용 시리얼라이저
    """
    
    class Meta:
        model = Comment
        fields = ['content', 'parent']
    
    def create(self, validated_data):
        # request에서 author와 post 설정
        validated_data['author'] = self.context['request'].user
        validated_data['post'] = self.context['post']
        return super().create(validated_data)


class PostListSerializer(serializers.ModelSerializer):
    """
    게시글 목록용 시리얼라이저
    
    간략한 정보만 포함
    """
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author', 'category',
            'thumbnail', 'published', 'views',
            'created_at', 'updated_at', 'comment_count'
        ]
    
    def get_comment_count(self, obj):
        return obj.get_comment_count()


class PostDetailSerializer(serializers.ModelSerializer):
    """
    게시글 상세용 시리얼라이저
    
    전체 내용 및 댓글 포함
    """
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    related_posts = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'content', 'author', 'category',
            'thumbnail', 'published', 'views',
            'created_at', 'updated_at',
            'comments', 'comment_count', 'related_posts'
        ]
    
    def get_comments(self, obj):
        """활성 댓글만 (부모 댓글만)"""
        comments = obj.comments.filter(is_active=True, parent__isnull=True)
        return CommentSerializer(comments, many=True).data
    
    def get_comment_count(self, obj):
        return obj.get_comment_count()
    
    def get_related_posts(self, obj):
        """관련 게시글 요약"""
        posts = obj.get_related_posts(limit=3)
        return PostListSerializer(posts, many=True).data


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """
    게시글 생성/수정용 시리얼라이저
    """
    category_id = serializers.IntegerField(required=False, allow_null=True)
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'category_id', 'thumbnail', 'published']
    
    def create(self, validated_data):
        category_id = validated_data.pop('category_id', None)
        validated_data['author'] = self.context['request'].user
        
        if category_id:
            validated_data['category_id'] = category_id
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        category_id = validated_data.pop('category_id', None)
        
        if category_id is not None:
            instance.category_id = category_id
        
        return super().update(instance, validated_data)
