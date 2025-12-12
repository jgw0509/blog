"""
Django 블로그 프로젝트 URL 설정
==============================
프로젝트 레벨 URL 라우팅
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

from blog.models import Post, Category, Comment
from accounts.models import User


def home_view(request):
    """홈페이지 뷰 - 최신 게시글, 카테고리, 통계 표시"""
    context = {
        'latest_posts': Post.objects.filter(published=True)
            .select_related('author', 'category')[:6],
        'categories': Category.objects.all(),
        'total_posts': Post.objects.filter(published=True).count(),
        'total_comments': Comment.objects.filter(is_active=True).count(),
        'total_users': User.objects.filter(is_active=True).count(),
    }
    return render(request, 'home.html', context)


urlpatterns = [
    # 관리자 페이지
    path('admin/', admin.site.urls),
    
    # 홈페이지
    path('', home_view, name='home'),
    
    # 사용자 인증
    path('accounts/', include('accounts.urls')),
    
    # 블로그 앱
    path('blog/', include('blog.urls')),
    
    # REST API
    path('api/', include('api.urls')),
]

# 개발 환경에서 미디어 파일 서빙
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# 관리자 사이트 커스터마이징
admin.site.site_header = '블로그 관리자'
admin.site.site_title = '블로그 관리'
admin.site.index_title = '관리자 대시보드'
