"""
Accounts 앱 - 뷰
================
사용자 인증 관련 뷰 정의
회원가입, 로그인, 로그아웃, 프로필, 팔로우, 알림 뷰
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import User, Follow, Notification
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm


class RegisterView(CreateView):
    """
    회원가입 뷰
    
    GET: 회원가입 폼 표시
    POST: 새 사용자 생성 및 자동 로그인
    """
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        """폼 유효성 검사 통과 시 사용자 생성 및 로그인"""
        response = super().form_valid(form)
        # 생성된 사용자로 자동 로그인
        login(self.request, self.object)
        messages.success(self.request, f'{self.object.username}님, 회원가입을 환영합니다!')
        return response
    
    def dispatch(self, request, *args, **kwargs):
        """이미 로그인한 사용자는 홈으로 리다이렉트"""
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(LoginView):
    """
    로그인 뷰
    
    Django 기본 LoginView 확장
    Bootstrap 스타일 폼 사용
    """
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        """로그인 성공 메시지"""
        messages.success(self.request, f'{form.get_user().username}님, 환영합니다!')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    """
    로그아웃 뷰
    
    로그아웃 후 홈으로 리다이렉트
    """
    next_page = reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        """로그아웃 메시지"""
        if request.user.is_authenticated:
            messages.info(request, '로그아웃되었습니다. 다시 만나요!')
        return super().dispatch(request, *args, **kwargs)


class ProfileView(DetailView):
    """
    프로필 조회 뷰
    
    사용자 프로필 상세 정보 표시
    작성한 게시글 목록 포함
    """
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        """추가 컨텍스트: 사용자의 게시글 목록 및 북마크 목록"""
        context = super().get_context_data(**kwargs)
        # 작성한 게시글
        context['user_posts'] = self.object.posts.filter(
            published=True
        ).select_related('category').order_by('-created_at')

        # 북마크한 게시글 (필터링 및 정렬 지원)
        search_query = self.request.GET.get('bookmark_q', '')
        sort_order = self.request.GET.get('bookmark_sort', '-created_at') # 기본값: 최신순

        bookmarked_posts = self.object.bookmarks.all()
        
        if search_query:
            bookmarked_posts = bookmarked_posts.filter(
                Q(post__title__icontains=search_query) | 
                Q(post__content__icontains=search_query)
            )
        
        context['bookmarked_posts'] = bookmarked_posts.select_related('post', 'post__author', 'post__category').order_by(sort_order)
        context['bookmark_q'] = search_query
        context['bookmark_sort'] = sort_order
        
        # 팔로우 상태
        if self.request.user.is_authenticated and self.request.user != self.object:
            context['is_following'] = self.request.user.is_following(self.object)
        else:
            context['is_following'] = False
        
        # 팔로워/팔로잉 수
        context['follower_count'] = self.object.get_follower_count()
        context['following_count'] = self.object.get_following_count()
        
        return context


class ProfileUpdateView(UpdateView):
    """
    프로필 수정 뷰
    
    본인만 수정 가능
    """
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'username': self.object.username})
    
    def dispatch(self, request, *args, **kwargs):
        """본인 확인"""
        obj = self.get_object()
        if obj != request.user:
            messages.error(request, '본인의 프로필만 수정할 수 있습니다.')
            return redirect('accounts:profile', username=obj.username)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, '프로필이 수정되었습니다.')
        return super().form_valid(form)


# ==================== 팔로우 관련 뷰 ====================

@login_required
@require_POST
def toggle_follow(request, username):
    """팔로우/언팔로우 토글"""
    target_user = get_object_or_404(User, username=username)
    
    if request.user == target_user:
        return JsonResponse({
            'success': False,
            'message': '자기 자신을 팔로우할 수 없습니다.'
        }, status=400)
    
    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target_user
    )
    
    if not created:
        follow.delete()
        following = False
        message = f'{target_user.username}님 팔로우를 취소했습니다.'
    else:
        following = True
        message = f'{target_user.username}님을 팔로우합니다.'
        # 알림 생성
        Notification.objects.create(
            recipient=target_user,
            sender=request.user,
            notification_type='follow',
            message=f'{request.user.username}님이 회원님을 팔로우합니다.'
        )
    
    return JsonResponse({
        'success': True,
        'following': following,
        'follower_count': target_user.get_follower_count(),
        'message': message
    })


@login_required
def follower_list(request, username):
    """팔로워 목록"""
    user = get_object_or_404(User, username=username)
    followers = user.followers.select_related('follower').order_by('-created_at')
    
    return render(request, 'accounts/follower_list.html', {
        'profile_user': user,
        'followers': followers
    })


@login_required
def following_list(request, username):
    """팔로잉 목록"""
    user = get_object_or_404(User, username=username)
    following = user.following.select_related('following').order_by('-created_at')
    
    return render(request, 'accounts/following_list.html', {
        'profile_user': user,
        'following': following
    })


# ==================== 알림 관련 뷰 ====================

@login_required
def notification_list(request):
    """알림 목록"""
    notifications = request.user.notifications.select_related(
        'sender', 'post', 'comment'
    ).order_by('-created_at')[:50]
    
    unread_count = request.user.get_unread_notification_count()
    
    return render(request, 'accounts/notification_list.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })


@login_required
@require_POST
def mark_notification_read(request, pk):
    """알림 읽음 처리"""
    notification = get_object_or_404(
        Notification, pk=pk, recipient=request.user
    )
    notification.mark_as_read()
    
    return JsonResponse({
        'success': True,
        'unread_count': request.user.get_unread_notification_count()
    })


@login_required
@require_POST
def mark_all_notifications_read(request):
    """모든 알림 읽음 처리"""
    request.user.notifications.filter(is_read=False).update(is_read=True)
    
    return JsonResponse({
        'success': True,
        'message': '모든 알림을 읽음 처리했습니다.'
    })


@login_required
def delete_notification(request, pk):
    """알림 삭제"""
    notification = get_object_or_404(
        Notification, pk=pk, recipient=request.user
    )
    notification.delete()
    messages.success(request, '알림이 삭제되었습니다.')
    return redirect('accounts:notification_list')

