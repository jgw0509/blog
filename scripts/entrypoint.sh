#!/bin/bash
set -e
echo "=========================================="
echo "Django 블로그 초기화 시작"
echo "=========================================="
echo ">> PostgreSQL 연결 대기 중..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    echo "   PostgreSQL이 아직 준비되지 않았습니다. 대기 중..."
    sleep 1
done
echo ">> PostgreSQL 연결 완료!"
cd /app/backend
echo ">> 마이그레이션 파일 생성..."
python manage.py makemigrations accounts --noinput
python manage.py makemigrations blog --noinput
python manage.py makemigrations --noinput
echo ">> 데이터베이스 마이그레이션 실행..."
python manage.py migrate --noinput
echo ">> 정적 파일 수집..."
python manage.py collectstatic --noinput
echo "=========================================="
echo "Django 블로그 초기화 완료!"
echo "=========================================="
if [ "$DEBUG" = "True" ]; then
    echo ">> 개발 서버 시작 (runserver)..."
    exec python manage.py runserver 0.0.0.0:8000
else
    echo ">> 프로덕션 서버 시작 (gunicorn)..."
    exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
fi
