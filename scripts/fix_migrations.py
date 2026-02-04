import os
import sys
import django
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

cursor = connection.cursor()
cursor.execute(
    "INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, %s)",
    ['accounts', '0001_initial', datetime.now()]
)
print('Migration accounts.0001_initial marked as applied successfully')
