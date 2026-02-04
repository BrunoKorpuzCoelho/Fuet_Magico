import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print("Current AUTH_USER_MODEL:", User)
print("\nChecking existing users...")

try:
    users = User.objects.all()
    print(f"\nTotal users: {users.count()}")
    
    for user in users:
        print(f"\nUsername: {user.username}")
        print(f"Email: {user.email}")
        print(f"Is superuser: {user.is_superuser}")
        print(f"Is staff: {user.is_staff}")
        if hasattr(user, 'role'):
            print(f"Role: {user.role}")
        
except Exception as e:
    print(f"Error: {e}")
