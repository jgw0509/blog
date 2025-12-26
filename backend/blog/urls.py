"""
Blog 앱 - URL 설정
==================
블로그 관련 URL 라우팅
"""

from django.urls import path, re_path
from . import views

app_name = 'blog'

urlpatterns = [
    # 관리자 대시보드
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    
    # 게시글 목록
    path('', views.PostListView.as_view(), name='post_list'),
    
    # 게시글 작성
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    
    # 카테고리 생성
    path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
    
    # 카테고리별 목록
    re_path(r'^category/(?P<slug>[\w-]+)/$', views.CategoryDetailView.as_view(), name='category_detail'),
    
    # ==================== 태그 관련 URL ====================
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    re_path(r'^tag/(?P<slug>[\w-]+)/$', views.TagDetailView.as_view(), name='tag_detail'),
    
    # ==================== 시리즈 관련 URL ====================
    path('series/', views.SeriesListView.as_view(), name='series_list'),
    path('series/create/', views.SeriesCreateView.as_view(), name='series_create'),
    re_path(r'^series/(?P<slug>[\w-]+)/$', views.SeriesDetailView.as_view(), name='series_detail'),
    
    # ==================== 임시저장 관련 URL ====================
    path('drafts/', views.draft_list, name='draft_list'),
    path('draft/<int:post_id>/delete/', views.delete_draft, name='delete_draft'),
    path('api/auto-save/', views.auto_save_post, name='auto_save'),
    
    # 댓글 삭제
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    
    # 게시글 상세 (유니코드 slug 지원)
    re_path(r'^(?P<slug>[\w-]+)/$', views.PostDetailView.as_view(), name='post_detail'),
    
    # 게시글 수정
    re_path(r'^(?P<slug>[\w-]+)/edit/$', views.PostUpdateView.as_view(), name='post_update'),
    
    # 게시글 삭제
    re_path(r'^(?P<slug>[\w-]+)/delete/$', views.PostDeleteView.as_view(), name='post_delete'),
    
    # 댓글 추가
    re_path(r'^(?P<slug>[\w-]+)/comment/$', views.add_comment, name='add_comment'),
    
    # 게시글 좋아요/싫어요
    re_path(r'^(?P<slug>[\w-]+)/like/$', views.toggle_post_like, name='post_like'),
    re_path(r'^(?P<slug>[\w-]+)/dislike/$', views.toggle_post_dislike, name='post_dislike'),
    
    # 댓글 좋아요/싫어요
    path('comment/<int:comment_id>/like/', views.toggle_comment_like, name='comment_like'),
    path('comment/<int:comment_id>/dislike/', views.toggle_comment_dislike, name='comment_dislike'),
    
    # 게시글 북마크
    re_path(r'^(?P<slug>[\w-]+)/bookmark/$', views.toggle_bookmark, name='post_bookmark'),
]

