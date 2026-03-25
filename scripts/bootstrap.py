#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
bootstrap.py
------------
Script de inicialização completa do sistema Fuet Mágico.

Verifica o estado actual e cria/actualiza todos os dados ESSENTIAL:
  1. Empresa default
  2. Utilizadores default (admin + manager)
  3. App Roles (permissões por utilizador/app)
  4. Blueprints de Atividades
  5. Cadeias de Automação
  6. Layout de Email
  7. Templates de Email

Uso:
  python scripts/bootstrap.py               # Verifica e cria tudo
  python scripts/bootstrap.py --check-only  # Apenas verifica, não cria
  python scripts/bootstrap.py --force       # Re-cria mesmo que já exista

Run from project root with venv activated.
"""

import os
import sys
import argparse
import importlib

# ── Setup Django ──────────────────────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

# ── Imports (after django.setup) ──────────────────────────────────────────────
from django.core.management import call_command
from apps.core.models import Company
from apps.accounts.models import CustomUser, AppRole, APP_REGISTRY
from apps.accounts.views import apply_default_app_roles  # noqa: E402

# ── Colours ───────────────────────────────────────────────────────────────────
GREEN  = '\033[92m'
YELLOW = '\033[93m'
RED    = '\033[91m'
BLUE   = '\033[94m'
BOLD   = '\033[1m'
RESET  = '\033[0m'

def ok(msg):    print(f"  {GREEN}✓{RESET}  {msg}")
def warn(msg):  print(f"  {YELLOW}⚠{RESET}  {msg}")
def err(msg):   print(f"  {RED}✗{RESET}  {msg}")
def info(msg):  print(f"  {BLUE}→{RESET}  {msg}")
def header(msg): print(f"\n{BOLD}{msg}{RESET}")
def sep():       print("  " + "─" * 56)


# ── Check helpers ─────────────────────────────────────────────────────────────

def check_company():
    """Verifica se a empresa default existe."""
    company = Company.objects.filter(name='Fuet Mágico').first()
    if company:
        ok(f"Empresa default encontrada: {company.name} (ID: {company.id})")
        return True
    warn("Empresa default 'Fuet Mágico' não existe.")
    return False


def check_users():
    """Verifica utilizadores default."""
    results = {}
    for username in ['cubix', 'daisy']:
        user = CustomUser.objects.filter(username=username).first()
        if user:
            company_count = user.companies.count()
            ok(f"User '{username}' existe  |  role={user.role}  |  empresas={company_count}")
            results[username] = user
        else:
            warn(f"User '{username}' não existe.")
            results[username] = None
    return results


def check_app_roles():
    """Verifica AppRoles por utilizador."""
    users = CustomUser.objects.prefetch_related('companies').all()
    all_ok = True
    for user in users:
        expected = user.companies.count() * len(APP_REGISTRY)
        actual = AppRole.objects.filter(user=user).count()
        if actual == 0 and expected > 0:
            warn(f"User '{user.username}' sem AppRoles (esperado ~{expected})")
            all_ok = False
        elif actual < expected:
            warn(f"User '{user.username}': {actual}/{expected} AppRoles")
            all_ok = False
        else:
            ok(f"User '{user.username}': {actual} AppRoles  ✓")
    return all_ok


def check_activity_templates():
    """Verifica ActivityType + ScheduledActivity blueprints."""
    try:
        from apps.core.models import ActivityType, ScheduledActivity
        type_count = ActivityType.objects.count()
        bp_count = ScheduledActivity.objects.count()
        if type_count > 0:
            ok(f"ActivityTypes: {type_count}  |  Blueprints: {bp_count}")
            return True
        warn("Sem ActivityTypes — blueprints por criar.")
        return False
    except Exception:
        warn("Não foi possível verificar blueprints de atividades.")
        return False


def check_activity_chains():
    """Verifica ActivityChain records."""
    try:
        from apps.core.models import ActivityChain
        count = ActivityChain.objects.count()
        if count > 0:
            ok(f"Cadeias de automação: {count} encontradas")
            return True
        warn("Sem cadeias de automação.")
        return False
    except Exception:
        warn("Não foi possível verificar cadeias de automação.")
        return False


def check_email_layout():
    """Verifica EmailLayout."""
    try:
        from apps.core.models import EmailLayout
        layout = EmailLayout.objects.first()
        if layout:
            ok(f"Layout de email encontrado (ID: {layout.id})")
            return True
        warn("Sem layout de email.")
        return False
    except Exception:
        warn("Não foi possível verificar layout de email.")
        return False


def check_email_templates():
    """Verifica EmailTemplate records."""
    try:
        from apps.core.models import EmailTemplate
        count = EmailTemplate.objects.count()
        if count > 0:
            ok(f"Templates de email: {count} encontrados")
            return True
        warn("Sem templates de email.")
        return False
    except Exception:
        warn("Não foi possível verificar templates de email.")
        return False


def check_warehouse():
    """Verifica se existe armazém default."""
    try:
        from apps.inventory.models import Warehouse
        wh = Warehouse.objects.filter(is_default=True).first()
        if wh:
            ok(f"Armazém default: '{wh.name}' (code={wh.code})")
            return True
        warn("Sem armazém default.")
        return False
    except Exception:
        warn("Não foi possível verificar armazém.")
        return False


# ── Run helpers ───────────────────────────────────────────────────────────────

def run_management_command(cmd, label):
    info(f"A executar: python manage.py {cmd}")
    try:
        call_command(cmd, verbosity=1)
        ok(f"{label} concluído.")
        return True
    except Exception as e:
        err(f"{label} falhou: {e}")
        return False


def run_script(module_path, label):
    info(f"A executar: {module_path}")
    try:
        mod = importlib.import_module(module_path)
        mod.run()
        ok(f"{label} concluído.")
        return True
    except Exception as e:
        err(f"{label} falhou: {e}")
        return False


def run_app_roles():
    """Aplica AppRoles a todos os utilizadores."""
    users = CustomUser.objects.prefetch_related('companies').all()
    total = 0
    for user in users:
        if not user.companies.exists():
            warn(f"User '{user.username}' sem empresas — AppRoles ignorados.")
            continue
        apply_default_app_roles(user)
        count = AppRole.objects.filter(user=user).count()
        ok(f"User '{user.username}': {count} AppRoles aplicados.")
        total += count
    ok(f"Total: {total} AppRoles criados/actualizados.")
    return True


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Bootstrap do sistema Fuet Mágico')
    parser.add_argument('--check-only', action='store_true', help='Apenas verifica, não cria nada')
    parser.add_argument('--force', action='store_true', help='Re-executa seeds mesmo que já existam')
    args = parser.parse_args()

    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}  🚀 FUET MÁGICO — Bootstrap{RESET}")
    print(f"{BOLD}{'='*60}{RESET}")

    if args.check_only:
        print(f"  {YELLOW}Modo: CHECK ONLY — nada será criado{RESET}\n")
    elif args.force:
        print(f"  {YELLOW}Modo: FORCE — re-executa mesmo que exista{RESET}\n")
    else:
        print(f"  {BLUE}Modo: NORMAL — cria apenas o que falta{RESET}\n")

    steps = [
        {
            'label': '1. Empresa Default',
            'check': check_company,
            'run': lambda: run_management_command('create_default_company', 'Empresa default'),
        },
        {
            'label': '2. Utilizadores Default',
            'check': lambda: all(check_users().values()),
            'run': lambda: run_management_command('create_default_users', 'Utilizadores default'),
        },
        {
            'label': '3. App Roles',
            'check': check_app_roles,
            'run': run_app_roles,
        },
        {
            'label': '4. Blueprints de Atividades',
            'check': check_activity_templates,
            'run': lambda: run_management_command('setup_activity_templates', 'Blueprints de atividades'),
        },
        {
            'label': '5. Cadeias de Automação',
            'check': check_activity_chains,
            'run': lambda: run_script('scripts.seed_activity_chains', 'Cadeias de automação'),
        },
        {
            'label': '6. Layout de Email',
            'check': check_email_layout,
            'run': lambda: run_script('scripts.seed_email_layout', 'Layout de email'),
        },
        {
            'label': '7. Templates de Email',
            'check': check_email_templates,
            'run': lambda: run_script('scripts.seed_email_templates', 'Templates de email'),
        },
        {
            'label': '8. Armazém Default',
            'check': check_warehouse,
            'run': lambda: run_script('scripts.seed_warehouse', 'Armazém default'),
        },
    ]

    results = {}

    for step in steps:
        header(step['label'])
        sep()
        exists = step['check']()
        results[step['label']] = exists

        if args.check_only:
            continue

        if exists and not args.force:
            info("Já existe — a saltar. (usa --force para re-executar)")
        else:
            success = step['run']()
            if success:
                results[step['label']] = True

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}  📋 Resumo{RESET}")
    print(f"{BOLD}{'='*60}{RESET}")
    for label, status in results.items():
        icon = f"{GREEN}✓{RESET}" if status else f"{YELLOW}⚠{RESET}"
        print(f"  {icon}  {label}")
    print(f"{BOLD}{'='*60}{RESET}\n")


if __name__ == '__main__':
    main()
