/*
==================================================
Django 블로그 JavaScript
==================================================
다크모드 토글
동적 기능
==================================================
*/

document.addEventListener('DOMContentLoaded', function() {
    
    // ===========================================
    // 다크모드 토글
    // ===========================================
    
    const themeToggle = document.getElementById('themeToggle');
    const html = document.documentElement;
    
    // 저장된 테마 또는 시스템 설정 적용
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme) {
        html.setAttribute('data-bs-theme', savedTheme);
    } else if (systemPrefersDark) {
        html.setAttribute('data-bs-theme', 'dark');
    }
    
    // 테마 아이콘 업데이트
    function updateThemeIcon() {
        const icon = themeToggle.querySelector('i');
        if (html.getAttribute('data-bs-theme') === 'dark') {
            icon.className = 'bi bi-sun-fill';
        } else {
            icon.className = 'bi bi-moon-stars-fill';
        }
    }
    
    updateThemeIcon();
    
    // 테마 토글
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = html.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            html.setAttribute('data-bs-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon();
        });
    }
    
    // ===========================================
    // 알림 자동 닫기
    // ===========================================
    
    const alerts = document.querySelectorAll('.alert:not(.alert-info):not(.alert-light)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000); // 5초 후 자동 닫기
    });
    
    // ===========================================
    // 외부 링크 새 탭에서 열기
    // ===========================================
    
    const externalLinks = document.querySelectorAll('a[href^="http"]');
    externalLinks.forEach(function(link) {
        if (!link.href.includes(window.location.hostname)) {
            link.setAttribute('target', '_blank');
            link.setAttribute('rel', 'noopener noreferrer');
        }
    });
    
    // ===========================================
    // 스크롤 시 네비게이션 바 그림자
    // ===========================================
    
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 10) {
                navbar.classList.add('shadow');
            } else {
                navbar.classList.remove('shadow');
            }
        });
    }
    
    // ===========================================
    // 이미지 레이지 로딩
    // ===========================================
    
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.add('fade-in');
                    observer.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(function(img) {
            imageObserver.observe(img);
        });
    }
    
    // ===========================================
    // 폼 유효성 검사 스타일
    // ===========================================
    
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                const originalHtml = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>처리 중...';
                
                // 폼 제출 후 버튼 복원 (실패 시)
                setTimeout(function() {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalHtml;
                }, 5000);
            }
        });
    });
    
    // ===========================================
    // 맨 위로 스크롤 버튼
    // ===========================================
    
    const scrollTopBtn = document.createElement('button');
    scrollTopBtn.className = 'btn btn-primary position-fixed bottom-0 end-0 m-4 rounded-circle d-none';
    scrollTopBtn.style.cssText = 'width: 48px; height: 48px; z-index: 1050;';
    scrollTopBtn.innerHTML = '<i class="bi bi-arrow-up"></i>';
    scrollTopBtn.setAttribute('title', '맨 위로');
    document.body.appendChild(scrollTopBtn);
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            scrollTopBtn.classList.remove('d-none');
        } else {
            scrollTopBtn.classList.add('d-none');
        }
    });
    
    scrollTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    console.log('Django Blog JS loaded successfully!');
});
