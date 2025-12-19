import os
import sys
import django

# Add backend directory to sys.path
backend_dir = os.path.join(os.getcwd(), 'backend')
sys.path.append(backend_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from blog.models import Post, Category
from django.contrib.auth import get_user_model

User = get_user_model()
try:
    admin = User.objects.get(username='jgw')
except User.DoesNotExist:
    admin = User.objects.first()

cat, _ = Category.objects.get_or_create(name='TestCat')

content = """
<h2>Introduction</h2>
Welcome to the rich content test. This is an automatically generated TOC test.
<h3>Details</h3>
Check out this Python code snippet:
<pre><code class="language-python">
def calculate_reading_time(text):
    words_per_minute = 225
    words = len(text.split())
    return words / words_per_minute
</code></pre>

<div class="callout callout-info">
    <i class="bi bi-info-circle callout-icon"></i>
    <div><strong>Tip:</strong> You can drag text to highlight it!</div>
</div>

<blockquote class="blockquote">
    "The more that you read, the more things you will know. The more that you learn, the more places you'll go." - Dr. Seuss
</blockquote>

<p>Try dragging this specific sentence to see the highlight tooltip in action.</p>
"""

p, created = Post.objects.get_or_create(
    slug='reading-test-rich',
    defaults={
        'title': 'Rich Content & Reading System Test',
        'content': content,
        'author': admin,
        'published': True,
        'category': cat
    }
)

if not created:
    p.title = 'Rich Content & Reading System Test'
    p.content = content
    p.save()

print(f'Test post created/updated: /blog/reading-test-rich/ by {admin.username}')
