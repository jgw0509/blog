import os

def update_js():
    js_path = 'backend/static/js/main.js'
    if not os.path.exists(js_path): return
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Toggle Logic (if missing)
    toggle_logic = """
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
"""

    # Phase 3: TOC & Highlighting Logic
    phase3_logic = """
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
"""

    if 'toggleReaderSettings' not in content:
        content = content.replace('applyTheme(currentTheme);', 'applyTheme(currentTheme);' + toggle_logic)
    
    if 'TOC' not in content:
         # Find a good place before the end
         content = content.replace('console.log(\'Django Blog JS loaded successfully!\');', phase3_logic + '    console.log(\'Django Blog JS loaded successfully!\');')

    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)

def update_css():
    css_path = 'backend/static/css/style.css'
    if not os.path.exists(css_path): return
    
    callout_styles = """
/* ===========================================
   고급 콘텐츠 스타일 (Callouts & Blockquotes)
   =========================================== */

.callout {
    padding: 1.25rem;
    margin-bottom: 1.5rem;
    border-radius: 0.75rem;
    border-left: 5px solid;
    display: flex;
    gap: 1rem;
    align-items: flex-start;
}

.callout-icon {
    font-size: 1.25rem;
    flex-shrink: 0;
}

.callout-info {
    background-color: rgba(13, 110, 253, 0.05);
    border-color: #0d6efd;
    color: var(--text-main);
}

.callout-warning {
    background-color: rgba(255, 193, 7, 0.05);
    border-color: #ffc107;
}

.callout-tip {
    background-color: rgba(25, 135, 84, 0.05);
    border-color: #198754;
}

blockquote {
    border-left: 4px solid var(--color-primary);
    padding: 1rem 1.5rem;
    margin: 1.5rem 0;
    background-color: var(--bg-body);
    font-style: italic;
    font-size: 1.1em;
    color: var(--text-muted);
}

.highlight-yellow { background-color: #fff3bf; color: #212529; }
.highlight-green { background-color: #d3f9d8; color: #212529; }
.highlight-pink { background-color: #ffdeeb; color: #212529; }

.toc-container {
    padding: 0;
}

.toc-link {
    display: block;
    padding: 0.35rem 0;
    color: var(--text-muted);
    text-decoration: none;
    font-size: 0.9rem;
    transition: all 0.2s;
    border-left: 2px solid transparent;
    padding-left: 1rem;
}

.toc-link:hover {
    color: var(--color-primary);
    background-color: rgba(0,0,0,0.02);
}

.toc-h3 { margin-left: 0; padding-left: 2rem; font-size: 0.85rem; }
"""

    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()

    if '고급 콘텐츠 스타일' not in css_content:
        with open(css_path, 'a', encoding='utf-8') as f:
            f.write(callout_styles)

if __name__ == "__main__":
    update_js()
    update_css()
    print("Update complete")
