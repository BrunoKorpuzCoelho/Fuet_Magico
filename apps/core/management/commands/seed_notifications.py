"""
Management command para criar notificações de teste.

Uso:
    python manage.py seed_notifications
    python manage.py seed_notifications --user cubix
    python manage.py seed_notifications --clear
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.core.models import Notification

User = get_user_model()


SEED_DATA = [
    # ── Urgentes (em atraso) ───────────────────────────────────────────────
    {
        'notification_type': 'ACTIVITY_OVERDUE',
        'title': 'Ligar para Alice Alves — atrasada 3 dias',
        'message': 'Atividade de follow-up no lead «Proposta Linha Fuet Premium» está em atraso.',
        'link': '/crm/leads/',
    },
    {
        'notification_type': 'ACTIVITY_OVERDUE',
        'title': 'Enviar proposta a Restaurante O Solar — atrasada 1 dia',
        'message': 'Prazo de envio de proposta comercial ultrapassado.',
        'link': '/crm/leads/',
    },
    {
        'notification_type': 'MENTION',
        'title': 'João mencionou-te numa nota',
        'message': 'em Lead «Valente Cunha S.A.»: @ti preciso da tua aprovação nesta proposta antes de enviar.',
        'link': '/crm/leads/',
    },

    # ── Para hoje ─────────────────────────────────────────────────────────
    {
        'notification_type': 'ACTIVITY_TODAY',
        'title': 'Follow-up com Daisy — prazo hoje',
        'message': 'Ligação de acompanhamento agendada para hoje com contacto Daisy.',
        'link': '/crm/leads/',
    },
    {
        'notification_type': 'ACTIVITY_TODAY',
        'title': 'Recolher documentos — Valente Cunha S.A.',
        'message': 'Entrega de documentação contratutal prevista para hoje.',
        'link': '/crm/leads/',
    },

    # ── Futuras ────────────────────────────────────────────────────────────
    {
        'notification_type': 'ACTIVITY_UPCOMING',
        'title': 'Reunião com Grupo Gastronómico Norte — amanhã',
        'message': 'Reunião de apresentação de catálogo agendada para amanhã às 10h.',
        'link': '/crm/leads/',
    },
    {
        'notification_type': 'ACTIVITY_UPCOMING',
        'title': 'Enviar amostras a Hotel Palácio — em 3 dias',
        'message': 'Preparar e enviar kit de amostras conforme acordado.',
        'link': '/crm/leads/',
    },

    # ── Sistema / outros ───────────────────────────────────────────────────
    {
        'notification_type': 'ASSIGNMENT',
        'title': 'Lead «Novos Sabores Lda» foi atribuída a ti',
        'message': 'O administrador atribuiu-te esta oportunidade. Verifica os detalhes.',
        'link': '/crm/leads/',
    },
    {
        'notification_type': 'STAGE_CHANGE',
        'title': 'Lead «Catering Algarve» passou para Proposta',
        'message': 'Etapa atualizada de Qualificação → Proposta.',
        'link': '/crm/leads/',
    },
    {
        'notification_type': 'WHATSAPP',
        'title': 'Nova mensagem WhatsApp — Alice Alves',
        'message': 'Olá! Já recebi a vossa proposta, posso falar segunda-feira?',
        'link': '/crm/leads/',
    },
    {
        'notification_type': 'COMMENT',
        'title': 'Maria respondeu à tua nota',
        'message': 'em Lead «Hotel Estrela»: Concordo, vou agendar a visita para a próxima semana.',
        'link': '/crm/leads/',
    },
    {
        'notification_type': 'SYSTEM',
        'title': 'Backup automático concluído',
        'message': 'Backup diário realizado com sucesso às 03:00.',
        'link': '',
    },
]


class Command(BaseCommand):
    help = 'Cria notificações de teste para o utilizador especificado (ou o primeiro superuser)'

    def add_arguments(self, parser):
        parser.add_argument('--user', type=str, default=None, help='Username do utilizador destino')
        parser.add_argument('--clear', action='store_true', help='Apagar notificações existentes antes de criar')

    def handle(self, *args, **options):
        username = options['user']

        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stderr.write(self.style.ERROR(f'Utilizador "{username}" não encontrado.'))
                return
        else:
            user = User.objects.filter(is_superuser=True).first() or User.objects.first()
            if not user:
                self.stderr.write(self.style.ERROR('Nenhum utilizador encontrado na base de dados.'))
                return

        if options['clear']:
            deleted, _ = Notification.objects.filter(user=user).delete()
            self.stdout.write(self.style.WARNING(f'Apagadas {deleted} notificações existentes para {user.username}.'))

        created = 0
        for item in SEED_DATA:
            Notification.objects.create(user=user, **item)
            created += 1

        self.stdout.write(self.style.SUCCESS(
            f'✅ {created} notificações de teste criadas para {user.username} ({user.get_full_name() or user.email}).'
        ))
