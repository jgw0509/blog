"""
Accounts 앱 - 뷰
================
사용자 인증 관련 뷰 정의
회원가입, 로그인, 로그아웃, 프로필 뷰
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy

from .models import User
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
        """추가 컨텍스트: 사용자의 게시글 목록"""
        context = super().get_context_data(**kwargs)
        # 작성한 게시글 (최신순 10개)
        context['user_posts'] = self.object.posts.filter(
            published=True
        ).select_related('category').order_by('-created_at')[:10]
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
