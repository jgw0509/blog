import os

def finalize_js():
    js_path = 'backend/static/js/main.js'
    if not os.path.exists(js_path): return
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()

    tooltip_logic = """
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
"""

    if '하이라이트 툴팁 로직' not in content:
        marker = 'console.log(\'Django Blog JS loaded successfully!\');'
        content = content.replace(marker, tooltip_logic + '\n    ' + marker)
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(content)

def finalize_css():
    css_path = 'backend/static/css/style.css'
    if not os.path.exists(css_path): return
    
    tooltip_styles = """
/* ===========================================
   하이라이트 툴팁 (Selection Tooltip)
   =========================================== */

.selection-tooltip {
    position: absolute;
    background-color: #1a1a1a;
    border-radius: 0.5rem;
    padding: 0.4rem;
    display: flex;
    gap: 0.5rem;
    align-items: center;
    z-index: 3000;
}

.selection-tooltip::after {
    content: '';
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    border-width: 6px;
    border-style: solid;
    border-color: #1a1a1a transparent transparent transparent;
}

.highlight-btn, .format-btn {
    padding: 0.25rem 0.5rem;
    border: none;
    background: transparent;
    transition: background 0.2s;
    color: white;
}

.highlight-btn:hover, .format-btn:hover {
    background-color: #333;
}

.color-dot {
    display: inline-block;
    width: 14px;
    height: 14px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.2);
}

.selection-tooltip .divider {
    width: 1px;
    height: 20px;
    background-color: #444;
    margin: 0 0.25rem;
}
"""

    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()

    if '하이라이트 툴팁' not in css_content:
        with open(css_path, 'a', encoding='utf-8') as f:
            f.write(tooltip_styles)

if __name__ == "__main__":
    finalize_js()
    finalize_css()
    print("Finalized Phase 3")
