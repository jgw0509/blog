"""
API 앱 - 뷰
==========
DRF ViewSet 기반 REST API
게시글, 댓글, 카테고리, 사용자 API
"""

from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from accounts.models import User
from accounts.serializers import (
    UserSerializer, RegisterSerializer, 
    LoginSerializer, PasswordChangeSerializer
)
from blog.models import Category, Post, Comment
from blog.serializers import (
    CategorySerializer,
    PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer,
    CommentSerializer, CommentCreateSerializer
)
from blog.filters import PostFilter, CommentFilter


# ===========================================
# 인증 API
# ===========================================

class RegisterAPIView(generics.CreateAPIView):
    """
    회원가입 API
    
    POST /api/auth/register/
    
    Request Body:
    - username: 사용자명
    - email: 이메일
    - password: 비밀번호
    - password2: 비밀번호 확인
    
    Response:
    - user: 생성된 사용자 정보
    - token: 인증 토큰
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # 토큰 생성
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': '회원가입이 완료되었습니다.'
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    """
    로그인 API
    
    POST /api/auth/login/
    
    Request Body:
    - username: 사용자명
    - password: 비밀번호
    
    Response:
    - user: 사용자 정보
    - token: 인증 토큰
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # 토큰 가져오기 또는 생성
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': '로그인되었습니다.'
        })


class LogoutAPIView(APIView):
    """
    로그아웃 API
    
    POST /api/auth/logout/
    
    토큰 삭제
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # 토큰 삭제
        request.user.auth_token.delete()
        return Response({'message': '로그아웃되었습니다.'})


class PasswordChangeAPIView(APIView):
    """
    비밀번호 변경 API
    
    POST /api/auth/password-change/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': '비밀번호가 변경되었습니다.'})


class CurrentUserAPIView(APIView):
    """
    현재 로그인 사용자 정보 API
    
    GET /api/auth/me/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response(UserSerializer(request.user).data)


# ===========================================
# 카테고리 API
# ===========================================

class CategoryViewSet(viewsets.ModelViewSet):
    """
    카테고리 ViewSet
    
    GET /api/categories/          - 목록
    GET /api/categories/{id}/     - 상세
    POST /api/categories/         - 생성 (관리자)
    PUT /api/categories/{id}/     - 수정 (관리자)
    DELETE /api/categories/{id}/  - 삭제 (관리자)
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        """읽기는 모든 사용자, 쓰기는 관리자만"""
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]


# ===========================================
# 게시글 API
# ===========================================

class PostViewSet(viewsets.ModelViewSet):
    """
    게시글 ViewSet
    
    GET /api/posts/              - 목록 (필터/검색 지원)
    GET /api/posts/{slug}/       - 상세
    POST /api/posts/             - 생성 (로그인)
    PUT /api/posts/{slug}/       - 수정 (작성자)
    DELETE /api/posts/{slug}/    - 삭제 (작성자)
    
    필터 파라미터:
    - search: 제목/내용 검색
    - category: 카테고리 슬러그
    - author: 작성자 username
    """
    queryset = Post.objects.filter(published=True)\
        .select_related('author', 'category')\
        .prefetch_related('comments')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = PostFilter
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'views', 'title']
    ordering = ['-created_at']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        return PostDetailSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # 자신의 비공개 게시글도 볼 수 있도록
        if self.request.user.is_authenticated:
            queryset = Post.objects.filter(
                published=True
            ) | Post.objects.filter(
                author=self.request.user
            )
            queryset = queryset.select_related('author', 'category')
        return queryset.distinct()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def update(self, request, *args, **kwargs):
        """본인 게시글만 수정 가능"""
        instance = self.get_object()
        if instance.author != request.user:
            return Response(
                {'error': '본인의 게시글만 수정할 수 있습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """본인 게시글만 삭제 가능"""
        instance = self.get_object()
        if instance.author != request.user:
            return Response(
                {'error': '본인의 게시글만 삭제할 수 있습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def increase_view(self, request, slug=None):
        """조회수 증가"""
        post = self.get_object()
        post.increase_views()
        return Response({'views': post.views})


# ===========================================
# 댓글 API
# ===========================================

class CommentViewSet(viewsets.ModelViewSet):
    """
    댓글 ViewSet
    
    GET /api/comments/              - 목록
    GET /api/comments/{id}/         - 상세
    POST /api/posts/{slug}/comments/ - 생성 (로그인)
    PUT /api/comments/{id}/         - 수정 (작성자)
    DELETE /api/comments/{id}/      - 삭제 (작성자)
    """
    queryset = Comment.objects.filter(is_active=True)\
        .select_related('author', 'post')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = CommentFilter
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer
    
    def update(self, request, *args, **kwargs):
        """본인 댓글만 수정 가능"""
        instance = self.get_object()
        if instance.author != request.user:
            return Response(
                {'error': '본인의 댓글만 수정할 수 있습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """본인 댓글만 삭제 가능 (비활성화)"""
        instance = self.get_object()
        if instance.author != request.user:
            return Response(
                {'error': '본인의 댓글만 삭제할 수 있습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostCommentAPIView(generics.ListCreateAPIView):
    """
    게시글 댓글 API
    
    GET /api/posts/{slug}/comments/  - 게시글 댓글 목록
    POST /api/posts/{slug}/comments/ - 댓글 작성
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_post(self):
        return get_object_or_404(Post, slug=self.kwargs['slug'], published=True)
    
    def get_queryset(self):
        post = self.get_post()
        return Comment.objects.filter(
            post=post, is_active=True, parent__isnull=True
        ).select_related('author')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['post'] = self.get_post()
        return context


# ===========================================
# 사용자 API
# ===========================================

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    사용자 ViewSet (읽기 전용)
    
    GET /api/users/              - 목록
    GET /api/users/{username}/   - 상세
    """
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [AllowAny]
