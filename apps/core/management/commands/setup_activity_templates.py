"""
Management command para popular os blueprints padrão de ScheduledActivity.

Usage:
    python manage.py setup_activity_templates
    python manage.py setup_activity_templates --clear  # Deletar blueprints existentes antes
"""
from django.core.management.base import BaseCommand
from apps.core.models import ActivityType, ScheduledActivity


class Command(BaseCommand):
    help = 'Criar blueprints padrão de ScheduledActivity com SVGs e cores'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Deletar todos os templates existentes antes de criar novos',
        )

    def handle(self, *args, **options):
        # ── Garantir que os tipos base existem ────────────────────────────
        DEFAULT_TYPES = [
            ('CALL',      'Phone Call'),
            ('EMAIL',     'Email'),
            ('MEETING',   'Meeting'),
            ('TODO',      'To-Do'),
            ('WHATSAPP',  'WhatsApp'),
            ('DOCUMENT',  'Document'),
            ('SIGNATURE', 'Signature'),
        ]
        type_map = {}
        for code, name in DEFAULT_TYPES:
            obj, created = ActivityType.objects.get_or_create(
                code=code,
                defaults={'name': name, 'is_active': True}
            )
            type_map[code] = obj
            status = '✅ Criado' if created else '— Já existe'
            self.stdout.write(f'  {status}: ActivityType "{name}" ({code})')
        self.stdout.write('')

        # SVGs (usando currentColor para cores dinâmicas)
        SVGS = {
            'first_contact': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="m24,2v4.5c0,.276-.224.5-.5.5s-.5-.224-.5-.5V2c0-.089-.012-.176-.034-.259l-7.112,7.112c-.098.098-.226.146-.354.146s-.256-.049-.354-.146c-.195-.195-.195-.512,0-.707l7.112-7.112c-.083-.022-.169-.034-.259-.034h-4.5c-.276,0-.5-.224-.5-.5s.224-.5.5-.5h4.5c1.103,0,2,.897,2,2Zm-.837,15.298c1.098,1.092,1.098,2.799.049,3.848l-.978,1.125c-1.121,1.124-2.608,1.729-4.211,1.729C10.275,24,0,13.725,0,5.976c0-1.603.605-3.089,1.704-4.187l1.176-1.024c.965-.97,2.764-.993,3.779.023l1.959,2.543c1.006,1,1.006,2.707-.043,3.756l-1.487,1.525c1.617,3.803,4.614,6.804,8.295,8.303l1.532-1.494c1.017-1.014,2.787-1.013,3.802.003l2.446,1.873Zm-.658.75l-2.446-1.873c-.736-.725-1.801-.682-2.439-.043,0,.002-1.771,1.727-1.771,1.727-.139.136-.343.18-.527.108-4.172-1.593-7.556-4.975-9.285-9.28-.074-.184-.032-.394.105-.536l1.722-1.766c.664-.664.664-1.736.005-2.396l-1.959-2.543c-.302-.299-.714-.452-1.133-.452-.436,0-.879.165-1.215.5l-1.176,1.025c-.885.885-1.386,2.121-1.386,3.456,0,7.16,9.864,17.024,17.023,17.024,1.335,0,2.571-.501,3.48-1.411l.978-1.125c.683-.685.683-1.757.023-2.416Z"/></svg>',
            
            'followup_call': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="m23.414.585c-.378-.377-.88-.585-1.413-.585h0l-6,.002c-1.103,0-2,.898-2,2.001l.002,7.858c0,.438.244.831.637,1.024.162.08.335.119.507.119.246,0,.489-.08.694-.237l2.302-1.767h5.858V2c0-.534-.208-1.036-.586-1.414Zm-.414,7.415h-5.198l-2.571,1.974c-.057.044-.112.034-.149.015-.036-.018-.079-.055-.079-.127l-.002-7.858c0-.552.448-1,1-1.001l6-.002h0c.267,0,.518.104.706.292.188.189.293.44.293.707v6Zm-8.849,9.213c-3.396-1.381-5.87-3.857-7.36-7.369l3.372-3.373L4.484.793,1.606,3.672c-1.036,1.033-1.606,2.432-1.606,3.941,0,7.198,9.188,16.386,16.387,16.386,1.508,0,2.908-.57,3.941-1.604l2.879-2.879-5.679-5.679-3.377,3.376Zm5.47,4.475c-.845.846-1.993,1.312-3.234,1.312C9.771,23,1,14.228,1,7.613c0-1.242.466-2.39,1.312-3.234l2.172-2.172,4.265,4.265-3.135,3.135.123.307c1.625,4.046,4.437,6.856,8.357,8.353l.303.115,3.131-3.13,4.265,4.265-2.172,2.172Z"/></svg>',
            
            'callback': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="m24,2v4.5c0,.276-.224.5-.5.5s-.5-.224-.5-.5V2c0-.089-.012-.176-.034-.259l-7.112,7.112c-.098.098-.226.146-.354.146s-.256-.049-.354-.146c-.195-.195-.195-.512,0-.707l7.112-7.112c-.083-.022-.169-.034-.259-.034h-4.5c-.276,0-.5-.224-.5-.5s.224-.5.5-.5h4.5c1.103,0,2,.897,2,2Zm-.837,15.298c1.098,1.092,1.098,2.799.049,3.848l-.978,1.125c-1.121,1.124-2.608,1.729-4.211,1.729C10.275,24,0,13.725,0,5.976c0-1.603.605-3.089,1.704-4.187l1.176-1.024c.965-.97,2.764-.993,3.779.023l1.959,2.543c1.006,1,1.006,2.707-.043,3.756l-1.487,1.525c1.617,3.803,4.614,6.804,8.295,8.303l1.532-1.494c1.017-1.014,2.787-1.013,3.802.003l2.446,1.873Zm-.658.75l-2.446-1.873c-.736-.725-1.801-.682-2.439-.043,0,.002-1.771,1.727-1.771,1.727-.139.136-.343.18-.527.108-4.172-1.593-7.556-4.975-9.285-9.28-.074-.184-.032-.394.105-.536l1.722-1.766c.664-.664.664-1.736.005-2.396l-1.959-2.543c-.302-.299-.714-.452-1.133-.452-.436,0-.879.165-1.215.5l-1.176,1.025c-.885.885-1.386,2.121-1.386,3.456,0,7.16,9.864,17.024,17.023,17.024,1.335,0,2.571-.501,3.48-1.411l.978-1.125c.683-.685.683-1.757.023-2.416Z"/></svg>',
            
            'no_answer': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="m14,1V0c5.514,0,10,4.486,10,10h-1c0-4.962-4.038-9-9-9Zm5,9h1c0-3.309-2.691-6-6-6v1c2.757,0,5,2.243,5,5Zm-1.473,3.837l5.679,5.679-2.879,2.879c-1.033,1.035-2.432,1.605-3.941,1.605C9.189,24,0,14.812,0,7.613,0,6.104.57,4.705,1.605,3.672L4.484.793l5.679,5.679-3.373,3.373c1.506,3.559,3.919,5.974,7.36,7.369l3.377-3.377Zm4.265,5.679l-4.265-4.265-3.13,3.131-.303-.116c-3.92-1.496-6.732-4.306-8.357-8.352l-.123-.307,3.135-3.135L4.484,2.207l-2.172,2.172c-.846.844-1.312,1.993-1.312,3.234,0,6.615,8.772,15.387,15.387,15.387,1.241,0,2.389-.466,3.233-1.312l2.172-2.172Z"/></svg>',
            
            'email': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M19.5,2H4.5C2.019,2,0,4.019,0,6.5v11c0,2.481,2.019,4.5,4.5,4.5h15c2.481,0,4.5-2.019,4.5-4.5V6.5c0-2.481-2.019-4.5-4.5-4.5ZM4.5,3h15c1.084,0,2.043,.506,2.686,1.283l-7.691,7.692c-.662,.661-1.557,1.025-2.497,1.025-.914-.017-1.826-.36-2.492-1.025L1.814,4.283c.643-.777,1.601-1.283,2.686-1.283Zm18.5,14.5c0,1.93-1.57,3.5-3.5,3.5H4.5c-1.93,0-3.5-1.57-3.5-3.5V6.5c0-.477,.097-.931,.271-1.346l7.528,7.528c.851,.851,1.98,1.318,3.177,1.318s2.375-.467,3.226-1.318l7.528-7.528c.174,.415,.271,.869,.271,1.346v11Z"/></svg>',
            
            'thankyou': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="m22.623,9.26l-1.623-1.564V3.5c0-1.93-1.57-3.5-3.5-3.5H6.5c-1.93,0-3.5,1.57-3.5,3.5v4.196l-1.623,1.564c-.875.844-1.377,2.024-1.377,3.24v7c0,2.481,2.019,4.5,4.5,4.5h15c2.481,0,4.5-2.019,4.5-4.5v-7c0-1.216-.502-2.396-1.377-3.24Zm-.693.721c.092.089.165.194.247.292l-1.177,1.177v-2.365l.93.896ZM4,3.5c0-1.379,1.121-2.5,2.5-2.5h11c1.379,0,2.5,1.121,2.5,2.5v8.949l-5.525,5.525c-1.322,1.322-3.627,1.322-4.949,0l-5.525-5.525V3.5Zm-1,5.585v2.365l-1.177-1.177c.081-.098.154-.203.247-.292l.93-.896Zm20,10.415c0,1.93-1.57,3.5-3.5,3.5H4.5c-1.93,0-3.5-1.57-3.5-3.5v-7c0-.469.097-.932.277-1.359l7.541,7.541c.85.851,1.979,1.318,3.182,1.318s2.332-.468,3.182-1.318l7.541-7.541c.18.427.277.89.277,1.359v7ZM6.659,8.163c-.202-.188-.214-.504-.025-.707.189-.201.505-.213.707-.025l2.278,2.117c.597.597,1.549.598,2.134.013l4.746-4.575c.198-.189.515-.186.707.014.191.198.186.515-.014.707l-4.739,4.568c-.482.483-1.12.725-1.759.725s-1.281-.243-1.77-.731l-2.266-2.104Z"/></svg>',
            
            'todo': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="m3.5,6c-.668,0-1.296-.26-1.768-.732L.167,3.873c-.207-.184-.225-.5-.041-.706.184-.207.5-.224.706-.041l1.586,1.414c.608.605,1.576.586,2.142.02l3.595-3.423c.199-.189.515-.183.707.018.19.2.183.517-.018.707l-3.586,3.414c-.463.463-1.091.724-1.759.724Zm20.5-1.5c0-.276-.224-.5-.5-.5h-11c-.276,0-.5.224-.5.5s.224.5.5.5h11c.276,0,.5-.224.5-.5ZM5.259,13.276l3.586-3.414c.2-.19.208-.507.018-.707-.192-.2-.508-.208-.707-.018l-3.595,3.423c-.566.566-1.555.566-2.121,0l-1.586-1.585c-.195-.195-.512-.195-.707,0s-.195.512,0,.707l1.586,1.585c.472.472,1.1.732,1.768.732s1.296-.26,1.759-.724Zm18.741-.776c0-.276-.224-.5-.5-.5h-11c-.276,0-.5.224-.5.5s.224.5.5.5h11c.276,0,.5-.224.5-.5ZM5.259,21.276l3.586-3.414c.2-.19.208-.507.018-.707-.192-.2-.508-.207-.707-.018l-3.595,3.423c-.566.566-1.534.586-2.142-.02l-1.586-1.414c-.206-.184-.521-.166-.706.041s-.166.522.041.706l1.565,1.395c.472.472,1.1.732,1.768.732s1.296-.26,1.759-.724Zm18.741-.776c0-.276-.224-.5-.5-.5h-11c-.276,0-.5.224-.5.5s.224.5.5.5h11c.276,0,.5-.224.5-.5Z"/></svg>',
            
            'whatsapp': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" fill-rule="evenodd" clip-rule="evenodd" d="M20.463,3.488C18.217,1.24,15.231,0.001,12.05,0 C5.495,0,0.16,5.334,0.157,11.892c-0.001,2.096,0.547,4.142,1.588,5.946L0.057,24l6.304-1.654 c1.737,0.948,3.693,1.447,5.683,1.448h0.005c6.554,0,11.89-5.335,11.893-11.893C23.944,8.724,22.708,5.735,20.463,3.488z M12.05,21.785h-0.004c-1.774,0-3.513-0.477-5.031-1.378l-0.361-0.214l-3.741,0.981l0.999-3.648l-0.235-0.374 c-0.99-1.574-1.512-3.393-1.511-5.26c0.002-5.45,4.437-9.884,9.889-9.884c2.64,0,5.122,1.03,6.988,2.898 c1.866,1.869,2.893,4.352,2.892,6.993C21.932,17.351,17.498,21.785,12.05,21.785z M17.472,14.382 c-0.297-0.149-1.758-0.868-2.031-0.967c-0.272-0.099-0.47-0.149-0.669,0.148s-0.767,0.967-0.941,1.166 c-0.173,0.198-0.347,0.223-0.644,0.074c-0.297-0.149-1.255-0.462-2.39-1.475c-0.883-0.788-1.48-1.761-1.653-2.059 s-0.018-0.458,0.13-0.606c0.134-0.133,0.297-0.347,0.446-0.521C9.87,9.97,9.919,9.846,10.019,9.647 c0.099-0.198,0.05-0.372-0.025-0.521C9.919,8.978,9.325,7.515,9.078,6.92c-0.241-0.58-0.486-0.501-0.669-0.51 C8.236,6.401,8.038,6.4,7.839,6.4c-0.198,0-0.52,0.074-0.792,0.372c-0.272,0.298-1.04,1.017-1.04,2.479 c0,1.463,1.065,2.876,1.213,3.074c0.148,0.198,2.095,3.2,5.076,4.487c0.709,0.306,1.263,0.489,1.694,0.626 c0.712,0.226,1.36,0.194,1.872,0.118c0.571-0.085,1.758-0.719,2.006-1.413c0.248-0.694,0.248-1.29,0.173-1.413 C17.967,14.605,17.769,14.531,17.472,14.382z"/></svg>',
            
            'document': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="m7,13h10v1H7v-1Zm0,5h7v-1h-7v1Zm15-10.707v16.707H2V2.5c0-1.378,1.122-2.5,2.5-2.5h10.207l7.293,7.293Zm-7-.293h5.293L15,1.707v5.293Zm6,16v-15h-7V1H4.5c-.827,0-1.5.673-1.5,1.5v20.5h18Z"/></svg>',
            
            'signature': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M24,15.5c0,.28-.22,.5-.5,.5h-7c-.83,0-1.5,.67-1.5,1.5s.67,1.5,1.5,1.5h3c1.38,0,2.5,1.12,2.5,2.5s-1.12,2.5-2.5,2.5H.5c-.28,0-.5-.22-.5-.5s.22-.5,.5-.5H19.5c.83,0,1.5-.67,1.5-1.5s-.67-1.5-1.5-1.5h-3c-1.38,0-2.5-1.12-2.5-2.5s1.12-2.5,2.5-2.5h7c.28,0,.5,.22,.5,.5ZM.15,19.85c-.12-.12-.17-.3-.13-.47l1.72-7.34c.3-1.29,1.28-2.34,2.55-2.74l3.94-1.24s0,0,0,0L15.52,.77c1.02-1.02,2.69-1.02,3.71,0,1.02,1.02,1.02,2.69,0,3.71l-7.29,7.29s0,0,0,0l-1.24,3.94c-.4,1.27-1.45,2.24-2.74,2.55l-7.34,1.72s-.08,.01-.11,.01c-.13,0-.26-.05-.35-.15ZM9.14,8.56l2.3,2.3,7.09-7.09c.63-.63,.63-1.67,0-2.3-.63-.63-1.67-.63-2.3,0l-7.09,7.09ZM1.39,17.91l3.76-3.76c.2-.2,.51-.2,.71,0s.2,.51,0,.71l-3.76,3.76,5.64-1.32c.95-.22,1.72-.94,2.02-1.87l1.16-3.68-2.65-2.65-3.68,1.16c-.93,.29-1.65,1.07-1.87,2.02l-1.32,5.64Z"/></svg>',
        }

        # Templates data
        templates_data = [
            # CALL (4)
            {
                'name': 'Primeira Ligação - Contacto Inicial',
                'activity_type': type_map['CALL'],
                'summary': 'Primeira ligação para {{contact_name}}',
                'description': 'Fazer contacto inicial, apresentar empresa e perceber necessidades',
                'icon_svg': SVGS['first_contact'],
                'icon_color': '#09C823',
            },
            {
                'name': 'Ligação de Follow-up',
                'activity_type': type_map['CALL'],
                'summary': 'Follow-up com {{contact_name}}',
                'description': 'Acompanhar proposta enviada e esclarecer dúvidas',
                'icon_svg': SVGS['followup_call'],
                'icon_color': '#0920C8',
            },
            {
                'name': 'Callback - Cliente Pediu para Ligar',
                'activity_type': type_map['CALL'],
                'summary': 'Ligar novamente para {{contact_name}}',
                'description': 'Cliente pediu para ligar de volta',
                'icon_svg': SVGS['callback'],
                'icon_color': '#C82909',
            },
            {
                'name': 'Retry - Não Atendeu',
                'activity_type': type_map['CALL'],
                'summary': 'Tentar contactar {{contact_name}} novamente',
                'description': 'Tentativa de contacto após não atender chamada anterior',
                'icon_svg': SVGS['no_answer'],
                'icon_color': '#F4D80B',
            },
            
            # EMAIL (4)
            {
                'name': 'Email de Boas-vindas',
                'activity_type': type_map['EMAIL'],
                'summary': 'Enviar email de boas-vindas para {{contact_name}}',
                'description': 'Email inicial com informações da empresa e próximos passos',
                'icon_svg': SVGS['email'],
                'icon_color': '#2CC809',
            },
            {
                'name': 'Enviar Proposta por Email',
                'activity_type': type_map['EMAIL'],
                'summary': 'Enviar proposta para {{company_name}}',
                'description': 'Enviar proposta comercial detalhada',
                'icon_svg': SVGS['email'],
                'icon_color': '#276CF5',
            },
            {
                'name': 'Email de Follow-up',
                'activity_type': type_map['EMAIL'],
                'summary': 'Follow-up email para {{contact_name}}',
                'description': 'Acompanhar interesse e responder questões',
                'icon_svg': SVGS['email'],
                'icon_color': '#F4EC0B',
            },
            {
                'name': 'Email de Agradecimento',
                'activity_type': type_map['EMAIL'],
                'summary': 'Agradecer {{contact_name}} pela reunião',
                'description': 'Email de agradecimento pós-reunião com resumo',
                'icon_svg': SVGS['thankyou'],
                'icon_color': '#2CC809',
            },
            
            # TODO (4)
            {
                'name': 'Pesquisar Cliente',
                'activity_type': type_map['TODO'],
                'summary': 'Pesquisar informações sobre {{company_name}}',
                'description': 'Pesquisar empresa, setor, concorrentes e decisores',
                'icon_svg': SVGS['todo'],
                'icon_color': '#276CF5',  # Azul
            },
            {
                'name': 'Preparar Proposta',
                'activity_type': type_map['TODO'],
                'summary': 'Preparar proposta para {{company_name}}',
                'description': 'Criar proposta comercial personalizada',
                'icon_svg': SVGS['todo'],
                'icon_color': '#2CC809',  # Verde
            },
            {
                'name': 'Atualizar CRM',
                'activity_type': type_map['TODO'],
                'summary': 'Atualizar informações de {{contact_name}} no CRM',
                'description': 'Registar notas e atualizar dados do lead/cliente',
                'icon_svg': SVGS['todo'],
                'icon_color': '#F4EC0B',  # Amarelo
            },
            {
                'name': 'Enviar Contrato',
                'activity_type': type_map['TODO'],
                'summary': 'Enviar contrato para {{company_name}}',
                'description': 'Preparar e enviar contrato para assinatura',
                'icon_svg': SVGS['todo'],
                'icon_color': '#8B5CF6',  # Roxo
            },
            
            # WHATSAPP (3)
            {
                'name': 'Follow-up via WhatsApp',
                'activity_type': type_map['WHATSAPP'],
                'summary': 'Mensagem WhatsApp para {{contact_name}}',
                'description': 'Follow-up rápido via WhatsApp',
                'icon_svg': SVGS['whatsapp'],
                'icon_color': '#2CC809',  # Verde
            },
            {
                'name': 'Solicitar Documentos - WhatsApp',
                'activity_type': type_map['WHATSAPP'],
                'summary': 'Pedir documentos a {{contact_name}} via WhatsApp',
                'description': 'Solicitar documentação necessária',
                'icon_svg': SVGS['whatsapp'],
                'icon_color': '#F4EC0B',  # Amarelo
            },
            {
                'name': 'Lembrete de Reunião - WhatsApp',
                'activity_type': type_map['WHATSAPP'],
                'summary': 'Lembrar {{contact_name}} da reunião',
                'description': 'Enviar lembrete de reunião agendada',
                'icon_svg': SVGS['whatsapp'],
                'icon_color': '#276CF5',  # Azul
            },
            
            # DOCUMENT (3)
            {
                'name': 'Recolher Documentos',
                'activity_type': type_map['DOCUMENT'],
                'summary': 'Recolher documentos de {{company_name}}',
                'description': 'Solicitar e recolher documentação necessária',
                'icon_svg': SVGS['document'],
                'icon_color': '#276CF5',  # Azul
            },
            {
                'name': 'Upload Certificação',
                'activity_type': type_map['DOCUMENT'],
                'summary': 'Upload certificado para {{company_name}}',
                'description': 'Fazer upload de certificações necessárias',
                'icon_svg': SVGS['document'],
                'icon_color': '#F4EC0B',  # Amarelo
            },
            {
                'name': 'Processar Fatura',
                'activity_type': type_map['DOCUMENT'],
                'summary': 'Processar fatura de {{company_name}}',
                'description': 'Verificar e processar fatura recebida',
                'icon_svg': SVGS['document'],
                'icon_color': '#2CC809',  # Verde
            },
            
            # SIGNATURE (3)
            {
                'name': 'Assinatura de Contrato',
                'activity_type': type_map['SIGNATURE'],
                'summary': 'Assinar contrato com {{company_name}}',
                'description': 'Obter assinatura do contrato comercial',
                'icon_svg': SVGS['signature'],
                'icon_color': '#276CF5',  # Azul (corrigido)
            },
            {
                'name': 'Assinatura de NDA',
                'activity_type': type_map['SIGNATURE'],
                'summary': 'Assinar NDA com {{company_name}}',
                'description': 'Obter assinatura de acordo de confidencialidade',
                'icon_svg': SVGS['signature'],
                'icon_color': '#F4EC0B',  # Amarelo
            },
            {
                'name': 'Assinatura de Acordo de Serviço',
                'activity_type': type_map['SIGNATURE'],
                'summary': 'Assinar acordo de serviço com {{company_name}}',
                'description': 'Obter assinatura do acordo de prestação de serviços',
                'icon_svg': SVGS['signature'],
                'icon_color': '#2CC809',  # Verde
            },
        ]

        # Clear existing templates if --clear flag
        if options['clear']:
            deleted_count = ScheduledActivity.objects.filter(owner_company__isnull=True).count()
            ScheduledActivity.objects.filter(owner_company__isnull=True).delete()
            self.stdout.write(
                self.style.WARNING(f'🗑️  Deletados {deleted_count} templates existentes')
            )

        # Create templates
        created_count = 0
        updated_count = 0
        
        for data in templates_data:
            template, created = ScheduledActivity.objects.update_or_create(
                name=data['name'],
                defaults=data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'\u2705 Criado: {template.name} ({template.activity_type.name})')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'\U0001f504 Atualizado: {template.name} ({template.activity_type.name})')
                )

        # Summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS(f'📊 RESUMO:'))
        self.stdout.write(self.style.SUCCESS(f'   ✅ Criados: {created_count}'))
        self.stdout.write(self.style.SUCCESS(f'   🔄 Atualizados: {updated_count}'))
        self.stdout.write(self.style.SUCCESS(f'   📋 Total: {created_count + updated_count}'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS('🎉 Blueprints de ScheduledActivity criados com sucesso!')
        )
