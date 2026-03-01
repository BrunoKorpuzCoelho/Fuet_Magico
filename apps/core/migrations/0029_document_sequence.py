import uuid
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_email_template_default_body_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentSequence',
            fields=[
                ('id',           models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ('created_at',   models.DateTimeField(auto_now_add=True)),
                ('updated_at',   models.DateTimeField(auto_now=True)),
                ('is_active',    models.BooleanField(default=True)),
                ('code',         models.CharField(
                    max_length=50,
                    verbose_name='Código',
                    help_text='Identificador único do tipo de documento (ex: WH_IN, SALE, INVOICE).',
                )),
                ('name',         models.CharField(max_length=100, verbose_name='Nome')),
                ('prefix',       models.CharField(
                    max_length=20, default='', verbose_name='Prefixo',
                    help_text='Texto que antecede o número (ex: WH/IN/).',
                )),
                ('suffix',       models.CharField(
                    max_length=20, blank=True, default='', verbose_name='Sufixo',
                    help_text='Texto após o número (ex: /2026). Normalmente vazio.',
                )),
                ('padding',      models.PositiveSmallIntegerField(
                    default=5, verbose_name='Dígitos',
                    help_text='Número de dígitos do contador (5 → 00001).',
                )),
                ('next_number',  models.PositiveIntegerField(default=1, verbose_name='Próximo número')),
                ('owner_company', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='document_sequences',
                    to='core.company',
                    verbose_name='Empresa',
                )),
            ],
            options={
                'verbose_name':        'Sequência de Documentos',
                'verbose_name_plural': 'Sequências de Documentos',
                'ordering':            ['code'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='documentsequence',
            unique_together={('code', 'owner_company')},
        ),
    ]
