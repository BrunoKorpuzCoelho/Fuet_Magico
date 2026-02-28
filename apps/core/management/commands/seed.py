# -*- coding: utf-8 -*-
"""
Management command: seed
========================
Executa seeds do sistema de forma centralizada.

Uso:
    python manage.py seed --essential        # Produção (só dados obrigatórios)
    python manage.py seed --demo             # Dados de demonstração
    python manage.py seed --all              # Tudo (essential + demo)
    python manage.py seed --only <key>       # Executa um seed específico
    python manage.py seed --list             # Lista todos os seeds
    python manage.py seed --demo --dry-run   # Mostra o que seria executado
"""

import importlib
import sys
import time

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from scripts.seed_registry import (
    SEEDS,
    SeedCategory,
    SeedEntry,
    get_demo_seeds,
    get_essential_seeds,
    get_seed_by_key,
    get_seeds,
)


class Command(BaseCommand):
    help = 'Executa seeds do sistema (essential, demo, ou ambos).'

    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--essential',
            action='store_true',
            help='Executa apenas seeds essenciais (produção).',
        )
        group.add_argument(
            '--demo',
            action='store_true',
            help='Executa apenas seeds de demonstração.',
        )
        group.add_argument(
            '--all',
            action='store_true',
            help='Executa todos os seeds (essential + demo).',
        )
        group.add_argument(
            '--only',
            type=str,
            metavar='KEY',
            help='Executa apenas o seed com esta chave (ex: email_layout).',
        )
        group.add_argument(
            '--list',
            action='store_true',
            help='Lista todos os seeds registados sem executar.',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostra o que seria executado sem realmente executar.',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Ignora avisos de seeds destrutivos (que apagam dados).',
        )

    def handle(self, *args, **options):
        if options['list']:
            return self._handle_list()

        if options['only']:
            entry = get_seed_by_key(options['only'])
            if not entry:
                available = ', '.join(s.key for s in SEEDS)
                raise CommandError(
                    f"Seed '{options['only']}' não encontrado.\n"
                    f"Seeds disponíveis: {available}"
                )
            entries = [entry]
        elif options['essential']:
            entries = get_essential_seeds()
        elif options['demo']:
            entries = get_demo_seeds()
        elif options['all']:
            entries = get_seeds()
        else:
            self.stderr.write(self.style.ERROR(
                'Especifica uma opção: --essential, --demo, --all, --only <key>, ou --list'
            ))
            return

        dry_run = options['dry_run']
        force = options['force']

        # Verifica seeds destrutivos
        destructive = [s for s in entries if s.destructive]
        if destructive and not dry_run and not force:
            self.stdout.write(self.style.WARNING(
                '\n⚠️  Os seguintes seeds são DESTRUTIVOS (apagam dados existentes):'
            ))
            for s in destructive:
                self.stdout.write(f'   • {s.key} — {s.name}')
            self.stdout.write('')
            confirm = input('Continuar? [y/N] ')
            if confirm.lower() not in ('y', 'yes', 's', 'sim'):
                self.stdout.write(self.style.WARNING('Cancelado.'))
                return

        # Header
        cat_label = 'TODOS' if options.get('all') else (
            entries[0].category.value.upper() if len(entries) == 1 and not options.get('only')
            else options.get('only', '').upper() if options.get('only')
            else entries[0].category.value.upper() if entries
            else '?'
        )
        if options.get('essential'):
            cat_label = 'ESSENTIAL'
        elif options.get('demo'):
            cat_label = 'DEMO'
        elif options.get('all'):
            cat_label = 'ESSENTIAL + DEMO'

        mode = ' (DRY RUN)' if dry_run else ''
        self.stdout.write('')
        self.stdout.write(self.style.HTTP_INFO(
            f'{"=" * 60}\n'
            f'  SEED RUNNER — {cat_label}{mode}\n'
            f'  {len(entries)} seed(s) a executar\n'
            f'{"=" * 60}'
        ))

        # Execução
        ok = 0
        failed = 0
        skipped = 0
        t_total = time.time()

        for entry in entries:
            tag = entry.category.value.upper()[:3]
            prefix = f'[{tag}] {entry.key}'

            if dry_run:
                flag = ' 💥 DESTRUTIVO' if entry.destructive else ''
                self.stdout.write(f'  {prefix} — {entry.name}{flag}')
                skipped += 1
                continue

            self.stdout.write('')
            self.stdout.write(self.style.HTTP_INFO(f'▶ {prefix} — {entry.name}'))
            if entry.description:
                self.stdout.write(f'  {entry.description}')

            t0 = time.time()
            try:
                self._run_seed(entry)
                elapsed = time.time() - t0
                self.stdout.write(self.style.SUCCESS(
                    f'  ✓ Concluído em {elapsed:.1f}s'
                ))
                ok += 1
            except Exception as exc:
                elapsed = time.time() - t0
                self.stderr.write(self.style.ERROR(
                    f'  ✗ ERRO após {elapsed:.1f}s: {exc}'
                ))
                failed += 1

        # Resumo
        total_elapsed = time.time() - t_total
        self.stdout.write('')
        self.stdout.write(self.style.HTTP_INFO(f'{"=" * 60}'))
        if dry_run:
            self.stdout.write(f'  DRY RUN: {skipped} seed(s) listados')
        else:
            parts = [f'{ok} OK']
            if failed:
                parts.append(f'{failed} falharam')
            self.stdout.write(f'  Resultado: {", ".join(parts)} ({total_elapsed:.1f}s)')
        self.stdout.write(self.style.HTTP_INFO(f'{"=" * 60}'))
        self.stdout.write('')

    def _handle_list(self):
        """Mostra lista formatada de todos os seeds."""
        self.stdout.write('')
        self.stdout.write(self.style.HTTP_INFO(f'{"=" * 70}'))
        self.stdout.write(self.style.HTTP_INFO('  SEED REGISTRY'))
        self.stdout.write(self.style.HTTP_INFO(f'{"=" * 70}'))

        for cat in SeedCategory:
            entries = get_seeds(cat)
            label = '🏭 ESSENTIAL (produção)' if cat == SeedCategory.ESSENTIAL else '🧪 DEMO (demonstração)'
            self.stdout.write('')
            self.stdout.write(self.style.WARNING(f'  {label}'))
            self.stdout.write(f'  {"─" * 50}')

            for s in entries:
                flags = []
                if s.destructive:
                    flags.append('💥')
                if s.is_management_command:
                    flags.append('cmd')
                else:
                    flags.append('script')
                flag_str = ' '.join(flags)
                self.stdout.write(
                    f'  {s.order:>3d}  {s.key:<25s} {flag_str:<10s} {s.name}'
                )
                if s.dependencies:
                    deps = ', '.join(s.dependencies)
                    self.stdout.write(f'       └─ depende de: {deps}')

        self.stdout.write('')
        total_e = len(get_essential_seeds())
        total_d = len(get_demo_seeds())
        self.stdout.write(f'  Total: {total_e} essential + {total_d} demo = {total_e + total_d} seeds')
        self.stdout.write(self.style.HTTP_INFO(f'{"=" * 70}'))
        self.stdout.write('')

    def _run_seed(self, entry: SeedEntry):
        """Executa um seed — management command ou script com run()."""
        if entry.is_management_command:
            self.stdout.write(f'  → manage.py {entry.runner}')
            call_command(entry.runner, verbosity=1)
        else:
            # Import dotted path: 'scripts.seed_email_layout' → module.run()
            self.stdout.write(f'  → {entry.runner}.run()')
            module = importlib.import_module(entry.runner)
            if not hasattr(module, 'run'):
                raise AttributeError(
                    f"Módulo '{entry.runner}' não tem função run(). "
                    f"Refactora o script para ter def run():."
                )
            module.run()
