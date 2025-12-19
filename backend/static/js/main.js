/*
==================================================
Django 블로그 JavaScript
==================================================
다크모드 토글
동적 기능
==================================================
*/

document.addEventListener('DOMContentLoaded', function () {

    // ===========================================
    // 테마 전환 (Light, Dark, Sepia)
    // ===========================================

    const themeToggle = document.getElementById('themeToggle');
    const html = document.documentElement;
    const themes = ['light', 'dark', 'sepia'];

    // 현재 테마 가져오기 (localStorage -> 시스템 설정 -> 기본값 'light')
    function getInitialTheme() {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme && themes.includes(savedTheme)) {
            return savedTheme;
        }
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        return systemPrefersDark ? 'dark' : 'light';
    }

    let currentTheme = getInitialTheme();

    // 테마 적용 함수
    function applyTheme(theme) {
        html.setAttribute('data-bs-theme', theme);
        localStorage.setItem('theme', theme);
        updateThemeUI(theme);
    }

    // 테마 UI(아이콘 및 툴팁) 업데이트
    function updateThemeUI(theme) {
        if (!themeToggle) return;
        const icon = themeToggle.querySelector('i');
        const labels = {
            'light': { icon: 'bi-sun-fill', text: '라이트 모드' },
            'dark': { icon: 'bi-moon-stars-fill', text: '다크 모드' },
            'sepia': { icon: 'bi-palette-fill', text: '세피아 모드' }
        };

        const config = labels[theme];
        icon.className = `bi ${config.icon}`;
        themeToggle.setAttribute('title', `테마 변경 (현재: ${config.text})`);
    }

    // 초기 테마 적용
    applyTheme(currentTheme);
    // 독서 설정창 토글
    const toggleReaderSettingsBtn = document.getElementById('toggleReaderSettings');
    const readerSettingsPanel = document.getElementById('readerSettingsPanel');
    if (toggleReaderSettingsBtn && readerSettingsPanel) {
        toggleReaderSettingsBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            readerSettingsPanel.classList.toggle('d-none');
        });
        
        document.addEventListener('click', function(e) {
            if (!readerSettingsPanel.contains(e.target) && e.target !== toggleReaderSettingsBtn) {
                readerSettingsPanel.classList.add('d-none');
            }
        });
    }


    // 테마 순환 토글 (Light -> Dark -> Sepia -> Light)
    if (themeToggle) {
        themeToggle.addEventListener('click', function () {
            const currentIndex = themes.indexOf(currentTheme);
            const nextIndex = (currentIndex + 1) % themes.length;
            currentTheme = themes[nextIndex];
            applyTheme(currentTheme);
    // 독서 설정창 토글
    const toggleReaderSettingsBtn = document.getElementById('toggleReaderSettings');
    const readerSettingsPanel = document.getElementById('readerSettingsPanel');
    if (toggleReaderSettingsBtn && readerSettingsPanel) {
        toggleReaderSettingsBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            readerSettingsPanel.classList.toggle('d-none');
        });
        
        document.addEventListener('click', function(e) {
            if (!readerSettingsPanel.contains(e.target) && e.target !== toggleReaderSettingsBtn) {
                readerSettingsPanel.classList.add('d-none');
            }
        });
    }

        });
    }

    // ===========================================
    // 알림 자동 닫기
    // ===========================================

    const alerts = document.querySelectorAll('.alert:not(.alert-info):not(.alert-light)');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000); // 5초 후 자동 닫기
    });

    // ===========================================
    // 외부 링크 새 탭에서 열기
    // ===========================================

    const externalLinks = document.querySelectorAll('a[href^="http"]');
    externalLinks.forEach(function (link) {
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
        window.addEventListener('scroll', function () {
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
        const imageObserver = new IntersectionObserver(function (entries, observer) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.add('fade-in');
                    observer.unobserve(img);
                }
            });
        });

        lazyImages.forEach(function (img) {
            imageObserver.observe(img);
        });
    }

    // ===========================================
    // 폼 유효성 검사 스타일
    // ===========================================

    const forms = document.querySelectorAll('form');
    forms.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                const originalHtml = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>처리 중...';

                // 폼 제출 후 버튼 복원 (실패 시)
                setTimeout(function () {
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

    window.addEventListener('scroll', function () {
        if (window.scrollY > 300) {
            scrollTopBtn.classList.remove('d-none');
        } else {
            scrollTopBtn.classList.add('d-none');
        }
    });

    scrollTopBtn.addEventListener('click', function () {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // ===========================================
    // 스크롤 진행 바 (Progress Bar)
    // ===========================================

    const progressBarFill = document.querySelector('.progress-bar-fill');
    if (progressBarFill) {
        window.addEventListener('scroll', function () {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            progressBarFill.style.width = scrolled + "%";
        });
    }

    // ===========================================
    // 독서 설정 (글자 크기, 줄 간격)
    // ===========================================

    const fontSizeBtns = document.querySelectorAll('.font-size-btn');
    const lineHeightBtns = document.querySelectorAll('.line-height-btn');
    const htmlRoot = document.documentElement;

    // 초기값 세팅 (localStorage)
    const savedFontSize = localStorage.getItem('reader-font-size') || '1.1rem';
    const savedLineHeight = localStorage.getItem('reader-line-height') || '1.8';

    htmlRoot.style.setProperty('--reader-font-size', savedFontSize);
    htmlRoot.style.setProperty('--reader-line-height', savedLineHeight);

    fontSizeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const size = btn.dataset.size;
            htmlRoot.style.setProperty('--reader-font-size', size);
            localStorage.setItem('reader-font-size', size);
            fontSizeBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });

    lineHeightBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const height = btn.dataset.height;
            htmlRoot.style.setProperty('--reader-line-height', height);
            localStorage.setItem('reader-line-height', height);
            lineHeightBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });

    // ===========================================
    // 예상 읽기 시간 계산
    // ===========================================

    const postContent = document.querySelector('.post-content');
    const readingTimeValue = document.getElementById('readingTimeValue');
    if (postContent && readingTimeValue) {
        const text = postContent.innerText;
        const wpm = 225; // 평균 읽기 속도
        const words = text.trim().split(/\s+/).length;
        const time = Math.ceil(words / wpm);
        readingTimeValue.innerText = time;
    }

    
    // ===========================================
    // 목차 (TOC) 자동 생성
    // ===========================================
    const tocContainer = document.querySelector('.toc-container');
    if (postContent && tocContainer) {
        const headings = postContent.querySelectorAll('h2, h3');
        if (headings.length > 0) {
            const tocList = document.createElement('nav');
            tocList.className = 'toc-list mb-3';
            headings.forEach((heading, index) => {
                const id = `heading-${index}`;
                heading.id = id;
                const link = document.createElement('a');
                link.href = `#${id}`;
                link.innerText = heading.innerText;
                link.className = `toc-link toc-${heading.tagName.toLowerCase()}`;
                
                // 스크롤 이동 시 부드럽게
                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    heading.scrollIntoView({ behavior: 'smooth' });
                });
                
                tocList.appendChild(link);
            });
            tocContainer.innerHTML = '<h6 class="mb-3">목차</h6>';
            tocContainer.appendChild(tocList);
        } else {
            const sideCard = tocContainer.closest('.card');
            if (sideCard) sideCard.style.display = 'none';
        }
    }

    // ===========================================
    // 텍스트 하이라이트 시스템
    // ===========================================
    if (postContent) {
        document.addEventListener('mouseup', function() {
            const selection = window.getSelection();
            const selectedText = selection.toString().trim();
            
            if (selectedText.length > 0) {
                // 여기서 툴팁을 띄울 수도 있지만, 우선 콘솔이나 간단한 스타일 적용 로직 확인
                // (사용자 요청: 형광펜 3색 등 적용 가능한 UI 필요)
            }
        });
    }
    
    // ===========================================
    // 하이라이트 툴팁 로직
    // ===========================================
    const tooltip = document.getElementById('selectionTooltip');
    const postContentArea = document.querySelector('.post-content');
    
    if (postContentArea && tooltip) {
        document.addEventListener('mouseup', function(e) {
            const selection = window.getSelection();
            const text = selection.toString().trim();
            
            if (text.length > 0 && postContentArea.contains(selection.anchorNode)) {
                const range = selection.getRangeAt(0);
                const rect = range.getBoundingClientRect();
                
                tooltip.style.left = `${rect.left + (rect.width / 2) - 80}px`;
                tooltip.style.top = `${rect.top + window.scrollY - 60}px`;
                tooltip.classList.remove('d-none');
            } else {
                if (!tooltip.contains(e.target)) {
                    tooltip.classList.add('d-none');
                }
            }
        });

        tooltip.querySelectorAll('.highlight-btn').forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                const color = btn.dataset.color;
                applyHighlight(`highlight-${color}`);
            });
        });

        tooltip.querySelectorAll('.format-btn').forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                const format = btn.dataset.format;
                if (format === 'italic') document.execCommand('italic');
                tooltip.classList.add('d-none');
            });
        });

        function applyHighlight(className) {
            const selection = window.getSelection();
            if (!selection.rangeCount) return;
            
            const range = selection.getRangeAt(0);
            const span = document.createElement('span');
            span.className = className;
            range.surroundContents(span);
            selection.removeAllRanges();
            tooltip.classList.add('d-none');
        }
    }

    console.log('Django Blog JS loaded successfully!');
});
