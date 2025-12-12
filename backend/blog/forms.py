"""
Blog 앱 - 폼
============
게시글, 댓글 폼 정의
Bootstrap 스타일 적용
"""

from django import forms
from .models import Post, Comment, Category


class PostForm(forms.ModelForm):
    """
    게시글 작성/수정 폼
    
    필드:
    - title: 제목
    - category: 카테고리 (선택)
    - content: 내용
    - thumbnail: 썸네일 이미지 (선택)
    - published: 발행 여부
    """
    
    class Meta:
        model = Post
        fields = ['title', 'category', 'content', 'thumbnail', 'published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '제목을 입력하세요'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '내용을 입력하세요',
                'rows': 15
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'title': '제목',
            'category': '카테고리',
            'content': '내용',
            'thumbnail': '썸네일',
            'published': '바로 발행',
        }


class CommentForm(forms.ModelForm):
    """
    댓글 작성 폼
    
    필드:
    - content: 댓글 내용
    """
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '댓글을 입력하세요',
                'rows': 3
            }),
        }
        labels = {
            'content': '',
        }


class CategoryForm(forms.ModelForm):
    """
    카테고리 생성 폼
    """
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '카테고리 이름을 입력하세요'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '카테고리 설명을 입력하세요 (선택)',
                'rows': 3
            }),
        }
        labels = {
            'name': '카테고리명',
            'description': '설명',
        }
