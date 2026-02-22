"""
seed_app_roles.py
-----------------
Backfill AppRole records for all existing users based on their system role.

Mapping:
  ADMIN    → admin   (full access to every app in every company)
  MANAGER  → manager (manager access to every app in every company)
  EMPLOYEE → user    (basic access to every app in every company)

Run from project root:
  python manage.py shell < scripts/seed_app_roles.py
  — or —
  python scripts/seed_app_roles.py   (if Django is on PYTHONPATH)
"""

import os
import sys
import django

# Ensure project root is on the path so 'config' is importable
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import CustomUser, AppRole, APP_REGISTRY
from apps.accounts.views import apply_default_app_roles

ROLE_LABEL = {
    CustomUser.ADMIN:    f'admin   → {AppRole.ADMIN}',
    CustomUser.MANAGER:  f'manager → {AppRole.MANAGER}',
    CustomUser.EMPLOYEE: f'employee→ {AppRole.USER}',
}

users = CustomUser.objects.prefetch_related('companies').all()
print(f"Found {users.count()} user(s).\n")

for user in users:
    companies = list(user.companies.all())
    label = ROLE_LABEL.get(user.role, f'unknown role ({user.role})')
    print(f"  [{label}]  {user.username}  —  {len(companies)} empresa(s)")
    if not companies:
        print("           ⚠ sem empresas associadas, nada a criar.")
        continue
    apply_default_app_roles(user)
    count = AppRole.objects.filter(user=user).count()
    print(f"           ✓ {count} AppRole(s) criados/actualizados.")

print("\nConcluído.")
