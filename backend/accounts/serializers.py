"""
Accounts 앱 - 시리얼라이저
==========================
DRF 시리얼라이저 정의
REST API를 통한 사용자 데이터 직렬화
"""

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    사용자 시리얼라이저
    
    읽기 전용: 사용자 정보 조회용
    비밀번호는 제외
    """
    
    post_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'profile_image', 'bio', 'date_joined',
            'post_count', 'comment_count'
        ]
        read_only_fields = ['id', 'date_joined']
    
    def get_post_count(self, obj):
        return obj.get_post_count()
    
    def get_comment_count(self, obj):
        return obj.get_comment_count()


class RegisterSerializer(serializers.ModelSerializer):
    """
    회원가입 시리얼라이저
    
    필드:
    - username: 사용자명 (필수)
    - email: 이메일 (필수)
    - password: 비밀번호 (필수, 쓰기 전용)
    - password2: 비밀번호 확인 (필수, 쓰기 전용)
    """
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
    
    def validate(self, attrs):
        """비밀번호 일치 검증"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': '비밀번호가 일치하지 않습니다.'
            })
        return attrs
    
    def validate_email(self, value):
        """이메일 중복 검증"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('이미 사용 중인 이메일입니다.')
        return value
    
    def create(self, validated_data):
        """사용자 생성"""
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    """
    로그인 시리얼라이저
    
    인증 정보 검증 후 사용자 반환
    """
    
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        user = authenticate(
            username=attrs['username'],
            password=attrs['password']
        )
        
        if not user:
            raise serializers.ValidationError('아이디 또는 비밀번호가 올바르지 않습니다.')
        
        if not user.is_active:
            raise serializers.ValidationError('비활성화된 계정입니다.')
        
        attrs['user'] = user
        return attrs


class PasswordChangeSerializer(serializers.Serializer):
    """
    비밀번호 변경 시리얼라이저
    """
    
    old_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password2 = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('현재 비밀번호가 올바르지 않습니다.')
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({
                'new_password': '새 비밀번호가 일치하지 않습니다.'
            })
        return attrs
    
    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
