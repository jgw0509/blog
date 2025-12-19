"""
Blog 앱 - 뷰
============
게시글, 댓글, 카테고리 관련 뷰
Class-Based Views 사용
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Category, Post, Comment, Bookmark
from .forms import PostForm, CommentForm, CategoryForm

class PostListView(ListView):
    """
    게시글 목록 뷰
    
    기능:
    - 발행된 게시글 목록 표시
    - 페이지네이션 (10개씩)
    - 카테고리 필터링
    - 검색 기능
    - 정렬 기능 (최신순/좋아요순)
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        """게시글 쿼리셋 - 필터링, 검색, 정렬 적용"""
        queryset = Post.objects.filter(published=True)\
            .select_related('author', 'category')\
            .prefetch_related('comments')\
            .annotate(likes_count=Count('likes'))
        
        # 카테고리 필터
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # 검색 필터
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(author__username__icontains=search_query)
            )
            
        # 정렬 필터
        sort = self.request.GET.get('sort', 'recent')
        if sort == 'likes':
            queryset = queryset.order_by('-likes_count', '-created_at')
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """추가 컨텍스트: 카테고리 목록, 검색어, 정렬 기준"""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('q', '')
        context['current_category'] = self.request.GET.get('category', '')
        context['current_sort'] = self.request.GET.get('sort', 'recent')
        return context


class PostDetailView(DetailView):
    """
    게시글 상세 뷰
    
    기능:
    - 게시글 본문 표시
    - 조회수 증가
    - 댓글 목록 표시
    - 관련 게시글 표시
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        """발행된 게시글만 조회 (작성자는 미발행도 볼 수 있음)"""
        if self.request.user.is_authenticated:
            return Post.objects.filter(
                Q(published=True) | Q(author=self.request.user)
            ).select_related('author', 'category')
        return Post.objects.filter(published=True).select_related('author', 'category')
    
    def get_object(self, queryset=None):
        """조회수 증가"""
        obj = super().get_object(queryset)
        obj.increase_views()
        return obj
    
    def get_context_data(self, **kwargs):
        """추가 컨텍스트: 댓글, 관련 게시글"""
        context = super().get_context_data(**kwargs)
        # 활성 댓글만 (부모 댓글만, 대댓글은 템플릿에서 처리)
        context['comments'] = self.object.comments.filter(
            is_active=True, parent__isnull=True
        ).select_related('author').prefetch_related('replies')
        context['comment_form'] = CommentForm()
        context['related_posts'] = self.object.get_related_posts()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    게시글 작성 뷰
    
    로그인 필수
    작성자 자동 설정
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """작성자를 현재 사용자로 설정"""
        form.instance.author = self.request.user
        messages.success(self.request, '게시글이 작성되었습니다.')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    게시글 수정 뷰
    
    로그인 필수
    본인 게시글만 수정 가능
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    slug_url_kwarg = 'slug'
    
    def test_func(self):
        """본인 게시글인지 확인"""
        post = self.get_object()
        return self.request.user == post.author
    
    def form_valid(self, form):
        messages.success(self.request, '게시글이 수정되었습니다.')
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    게시글 삭제 뷰
    
    로그인 필수
    본인 게시글만 삭제 가능
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    slug_url_kwarg = 'slug'
    
    def test_func(self):
        """본인 게시글인지 확인"""
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, '게시글이 삭제되었습니다.')
        return super().delete(request, *args, **kwargs)


class CategoryDetailView(ListView):
    """
    카테고리별 게시글 목록 뷰
    """
    model = Post
    template_name = 'blog/category_detail.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(
            category=self.category, published=True
        ).select_related('author')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        return context


@login_required
def add_comment(request, slug):
    """
    댓글 추가 뷰
    
    POST 요청으로만 처리
    부모 댓글 ID가 있으면 대댓글로 처리
    """
    post = get_object_or_404(Post, slug=slug, published=True)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            
            # 대댓글 처리
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent = get_object_or_404(Comment, id=parent_id)
                comment.parent = parent
            
            comment.save()
            messages.success(request, '댓글이 작성되었습니다.')
    
    return redirect('blog:post_detail', slug=slug)


@login_required
def delete_comment(request, comment_id):
    """
    댓글 삭제 (비활성화) 뷰
    
    본인 댓글만 삭제 가능
    """
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.author != request.user:
        messages.error(request, '본인의 댓글만 삭제할 수 있습니다.')
    else:
        comment.is_active = False
        comment.save()
        messages.success(request, '댓글이 삭제되었습니다.')
    
    return redirect('blog:post_detail', slug=comment.post.slug)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    """
    카테고리 생성 뷰
    
    로그인 필수
    """
    model = Category
    form_class = CategoryForm
    template_name = 'blog/category_form.html'
    success_url = reverse_lazy('blog:post_create')
    
    def form_valid(self, form):
        messages.success(self.request, '새 카테고리가 생성되었습니다.')
        return super().form_valid(form)


@login_required
@require_POST
def toggle_post_like(request, slug):
    """게시글 좋아요 토글"""
    post = get_object_or_404(Post, slug=slug)
    user = request.user
    
    if post.dislikes.filter(id=user.id).exists():
        post.dislikes.remove(user)
    
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
        
    return JsonResponse({
        'liked': liked,
        'likes_count': post.likes.count(),
        'dislikes_count': post.dislikes.count()
    })


@login_required
@require_POST
def toggle_post_dislike(request, slug):
    """게시글 싫어요 토글"""
    post = get_object_or_404(Post, slug=slug)
    user = request.user
    
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
    
    if post.dislikes.filter(id=user.id).exists():
        post.dislikes.remove(user)
        disliked = False
    else:
        post.dislikes.add(user)
        disliked = True
        
    return JsonResponse({
        'disliked': disliked,
        'likes_count': post.likes.count(),
        'dislikes_count': post.dislikes.count()
    })


@login_required
@require_POST
def toggle_comment_like(request, comment_id):
    """댓글 좋아요 토글"""
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user
    
    if comment.dislikes.filter(id=user.id).exists():
        comment.dislikes.remove(user)
    
    if comment.likes.filter(id=user.id).exists():
        comment.likes.remove(user)
        liked = False
    else:
        comment.likes.add(user)
        liked = True
        
    return JsonResponse({
        'liked': liked,
        'likes_count': comment.likes.count(),
        'dislikes_count': comment.dislikes.count()
    })


@login_required
@require_POST
def toggle_comment_dislike(request, comment_id):
    """댓글 싫어요 토글"""
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user
    
    if comment.likes.filter(id=user.id).exists():
        comment.likes.remove(user)
    
    if comment.dislikes.filter(id=user.id).exists():
        comment.dislikes.remove(user)
        disliked = False
    else:
        comment.dislikes.add(user)
        disliked = True
        
    return JsonResponse({
        'disliked': disliked,
        'likes_count': comment.likes.count(),
        'dislikes_count': comment.dislikes.count()
    })


@login_required
@require_POST
def toggle_bookmark(request, slug):
    """게시글 북마크 토글"""
    post = get_object_or_404(Post, slug=slug)
    user = request.user
    
    bookmark, created = Bookmark.objects.get_or_create(user=user, post=post)
    
    if not created:
        bookmark.delete()
        saved = False
    else:
        saved = True
        
    return JsonResponse({
        'saved': saved,
        'message': '북마크에 저장되었습니다.' if saved else '북마크가 취소되었습니다.'
    })

