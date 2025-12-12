# ===========================================
# Django 블로그 프로젝트 Dockerfile
# ===========================================

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    dos2unix \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# pip 업그레이드
RUN pip install --upgrade pip

# Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 파일 복사
COPY . .

# Windows CRLF -> Unix LF 변환 및 실행 권한 부여
RUN dos2unix /app/scripts/entrypoint.sh && chmod +x /app/scripts/entrypoint.sh

# 정적/미디어 파일 디렉토리 생성
RUN mkdir -p /app/backend/staticfiles /app/backend/media

# 포트 노출
EXPOSE 8000

# 컨테이너 시작 명령
ENTRYPOINT ["/app/scripts/entrypoint.sh"]
