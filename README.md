# Django 블로그 프로젝트

Django, Docker, PostgreSQL, Bootstrap 5를 사용한 완전한 블로그 웹사이트입니다.

## 🚀 주요 기능

- **사용자 인증**: 회원가입, 로그인, 로그아웃, 프로필 관리
- **게시글 관리**: CRUD (생성, 조회, 수정, 삭제)
- **댓글 시스템**: 댓글 및 대댓글 지원
- **카테고리 분류**: 게시글 카테고리 필터링
- **검색 기능**: 제목/내용 검색
- **REST API**: Django REST Framework 기반 API
- **반응형 디자인**: Bootstrap 5, 모바일 최적화
- **다크 모드**: 시스템 설정 연동

## 📁 프로젝트 구조

```
blog/
├── docker-compose.yml     # Docker 서비스 구성
├── Dockerfile             # Django 이미지 빌드
├── requirements.txt       # Python 패키지 목록
├── .env.example           # 환경변수 템플릿
├── .gitignore
│
├── backend/
│   ├── manage.py
│   ├── config/            # Django 프로젝트 설정
│   ├── accounts/          # 사용자 인증 앱
│   ├── blog/              # 블로그 핵심 앱
│   ├── api/               # REST API 앱
│   ├── templates/         # HTML 템플릿
│   └── static/            # CSS, JS, 이미지
│
└── scripts/
    └── entrypoint.sh      # Docker 진입점
```

## 🛠 기술 스택

| 분류 | 기술 |
|------|------|
| Backend | Django 5.0 (LTS) |
| Database | PostgreSQL (latest) |
| API | Django REST Framework |
| Frontend | Bootstrap 5, HTML5, CSS3 |
| Container | Docker, Docker Compose |
| Server | Gunicorn (Production) |

## ⚡ 빠른 시작

### 1. 저장소 클론

```bash
git clone <repository-url>
cd blog
```

### 2. 환경변수 설정

```bash
cp .env.example .env
```

`.env` 파일을 열어 필요한 값을 수정하세요:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
POSTGRES_PASSWORD=your-secure-password
```

### 3. Docker 빌드 및 실행

```bash
# 빌드 및 백그라운드 실행
docker-compose up -d --build

# 로그 확인
docker-compose logs -f web
```

### 4. 데이터베이스 초기화

```bash
# 마이그레이션 (자동 실행됨)
docker-compose exec web python manage.py migrate

# 슈퍼유저 생성
docker-compose exec web python manage.py createsuperuser
```

### 5. 접속

- 블로그: http://localhost:8000/
- 관리자: http://localhost:8000/admin/
- API: http://localhost:8000/api/

## 📚 API 엔드포인트

### 인증
| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/api/auth/register/` | 회원가입 |
| POST | `/api/auth/login/` | 로그인 |
| POST | `/api/auth/logout/` | 로그아웃 |
| GET | `/api/auth/me/` | 현재 사용자 |

### 게시글
| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/api/posts/` | 게시글 목록 |
| POST | `/api/posts/` | 게시글 생성 |
| GET | `/api/posts/{slug}/` | 게시글 상세 |
| PUT | `/api/posts/{slug}/` | 게시글 수정 |
| DELETE | `/api/posts/{slug}/` | 게시글 삭제 |

### 카테고리
| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/api/categories/` | 카테고리 목록 |
| GET | `/api/categories/{slug}/` | 카테고리 상세 |

### 검색 및 필터
```
GET /api/posts/?search=검색어
GET /api/posts/?category=tech
GET /api/posts/?author=username
```

## 🔒 보안 설정

### 개발 환경
- DEBUG=True
- CORS 모든 오리진 허용
- HTTP 사용

### 운영 환경
- DEBUG=False 필수!
- SECRET_KEY 새로 생성
- HTTPS 강제 (SECURE_SSL_REDIRECT)
- HSTS, XSS 필터 활성화
- CORS 허용 도메인 제한

```python
# settings.py (운영 환경)
DEBUG = False
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 🧪 개발 명령어

```bash
# 컨테이너 접속
docker-compose exec web bash

# 마이그레이션 생성
docker-compose exec web python manage.py makemigrations

# 정적 파일 수집
docker-compose exec web python manage.py collectstatic

# 쉘 접속
docker-compose exec web python manage.py shell

# 테스트 실행
docker-compose exec web python manage.py test

# 컨테이너 중지
docker-compose down

# 볼륨 포함 삭제
docker-compose down -v
```

## 📝 커스터마이징

### 카테고리 추가 (관리자 페이지)
1. `/admin/` 접속
2. 블로그 > 카테고리 추가

### 테마 수정
`backend/static/css/style.css` 파일에서 CSS 변수 수정:

```css
:root {
    --color-primary: #4f46e5;  /* 메인 색상 변경 */
}
```

## 🤝 기여

1. Fork
2. Feature 브랜치 생성 (`git checkout -b feature/AmazingFeature`)
3. 커밋 (`git commit -m 'Add some AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Pull Request

## 📄 라이선스

MIT License

---

Made with ❤️ using Django
