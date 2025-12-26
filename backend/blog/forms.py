"""
Blog 앱 - 폼
============
게시글, 댓글 폼 정의
Bootstrap 스타일 적용
"""

from django import forms
from .models import Post, Comment, Category, Tag, PostSeries


from django_summernote.widgets import SummernoteWidget

class PostForm(forms.ModelForm):
    """
    게시글 작성/수정 폼
    
    필드:
    - title: 제목
    - category: 카테고리 (선택)
    - tags: 태그 (선택, 다중)
    - series: 시리즈 (선택)
    - content: 내용
    - thumbnail: 썸네일 이미지 (선택)
    - published: 발행 여부
    """
    
    # 태그 입력 필드 (쉼표로 구분)
    tags_input = forms.CharField(
        label='태그',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '태그를 쉼표로 구분하여 입력 (예: Python, Django, 웹개발)'
        }),
        help_text='태그를 쉼표(,)로 구분하여 입력하세요'
    )
    
    class Meta:
        model = Post
        fields = ['title', 'category', 'series', 'content', 'thumbnail', 'published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '제목을 입력하세요'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'series': forms.Select(attrs={
                'class': 'form-select'
            }),
            'content': SummernoteWidget(),
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
            'series': '시리즈',
            'content': '내용',
            'thumbnail': '썸네일',
            'published': '바로 발행',
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # 사용자의 시리즈만 표시
        if user:
            self.fields['series'].queryset = PostSeries.objects.filter(author=user)
        
        # 기존 태그 로드
        if self.instance.pk:
            self.fields['tags_input'].initial = ', '.join(
                tag.name for tag in self.instance.tags.all()
            )
    
    def save(self, commit=True):
        instance = super().save(commit=commit)
        
        if commit:
            # 태그 처리
            tags_text = self.cleaned_data.get('tags_input', '')
            if tags_text:
                tag_names = [t.strip() for t in tags_text.split(',') if t.strip()]
                instance.tags.clear()
                for name in tag_names:
                    tag, created = Tag.objects.get_or_create(
                        name=name,
                        defaults={'slug': ''}
                    )
                    instance.tags.add(tag)
            else:
                instance.tags.clear()
        
        return instance


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


class PostSeriesForm(forms.ModelForm):
    """
    시리즈 생성/수정 폼
    """
    class Meta:
        model = PostSeries
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '시리즈 제목을 입력하세요'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '시리즈 설명을 입력하세요 (선택)',
                'rows': 3
            }),
        }
        labels = {
            'title': '시리즈 제목',
            'description': '설명',
        }

