import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.core.management import call_command

print('Compiling English translations...')
call_command('compilemessages', locale=['en'], verbosity=2)

print('\nCompiling French translations...')
call_command('compilemessages', locale=['fr'], verbosity=2)

print('\n✅ All translations compiled successfully!')
