import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from config.tasks import test_celery_task

print("🚀 Sending test task to Celery...")
result = test_celery_task.delay("Hello from Fuet Mágico!")
print(f"✅ Task sent! Task ID: {result.id}")
print(f"📊 Check Celery worker terminal for execution logs")
