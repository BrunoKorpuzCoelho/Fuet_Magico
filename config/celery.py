import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('fuet_magico')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# ---------------------------------------------------------------------------
# Beat schedule — tarefas periódicas
# ---------------------------------------------------------------------------

app.conf.beat_schedule = {
    # Verifica o IMAP de todos os utilizadores ativos a cada 5 minutos
    'poll-imap-every-5-min': {
        'task'    : 'config.tasks.poll_imap_all_active_users',
        'schedule': 300.0,  # segundos
    },
    # Verifica stock abaixo do mínimo de 4 em 4 horas
    'check-low-stock-every-4h': {
        'task'    : 'config.tasks.check_low_stock_periodic',
        'schedule': 14400.0,  # 4 horas em segundos
    },
}
app.conf.timezone = 'UTC'


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

