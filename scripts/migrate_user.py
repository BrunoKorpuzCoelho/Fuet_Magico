import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

cursor = connection.cursor()

cursor.execute("""
    INSERT INTO accounts_customuser 
    (password, last_login, is_superuser, username, first_name, last_name, 
     email, is_staff, is_active, date_joined, phone, avatar, role)
    SELECT 
        password, last_login, is_superuser, username, first_name, last_name,
        email, is_staff, is_active, date_joined, NULL, NULL, 'ADMIN'
    FROM auth_user
    WHERE username = 'cubix'
""")

cursor.execute("""
    INSERT INTO accounts_customuser_groups (customuser_id, group_id)
    SELECT 
        (SELECT id FROM accounts_customuser WHERE username = 'cubix'),
        group_id
    FROM auth_user_groups
    WHERE user_id = (SELECT id FROM auth_user WHERE username = 'cubix')
""")

cursor.execute("""
    INSERT INTO accounts_customuser_user_permissions (customuser_id, permission_id)
    SELECT 
        (SELECT id FROM accounts_customuser WHERE username = 'cubix'),
        permission_id
    FROM auth_user_user_permissions
    WHERE user_id = (SELECT id FROM auth_user WHERE username = 'cubix')
""")

print('✅ User "cubix" migrated successfully to accounts_customuser')
print('📧 Email: admin@fuetmagico.pt')
print('👤 Role: ADMIN')
print('🔑 Password: (preserved from auth_user)')
