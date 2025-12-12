"""
Accounts 앱 - 폼
================
사용자 인증 관련 폼 정의
회원가입, 로그인, 프로필 수정 폼
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    회원가입 폼
    
    필드:
    - username: 사용자명. unique
    - email: 이메일 (필수)
    - password1: 비밀번호
    - password2: 비밀번호 확인
    """
    
    email = forms.EmailField(
        label=_('이메일'),
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': '이메일을 입력하세요',
            'autocomplete': 'email'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bootstrap 클래스 적용
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '사용자명을 입력하세요'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '비밀번호를 입력하세요'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '비밀번호를 다시 입력하세요'
        })
    
    def clean_email(self):
        """이메일 중복 검사"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('이미 사용 중인 이메일 주소입니다.'))
        return email


class CustomAuthenticationForm(AuthenticationForm):
    """
    로그인 폼
    
    Bootstrap 스타일 적용
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '사용자명을 입력하세요',
            'autofocus': True
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '비밀번호를 입력하세요'
        })


class UserProfileForm(forms.ModelForm):
    """
    프로필 수정 폼
    
    수정 가능 필드:
    - first_name: 이름
    - last_name: 성
    - email: 이메일
    - profile_image: 프로필 이미지
    - bio: 자기소개
    """
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'profile_image', 'bio')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '이름'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '성'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': '이메일'
            }),
            'profile_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '자기소개를 입력하세요',
                'rows': 4
            }),
        }
