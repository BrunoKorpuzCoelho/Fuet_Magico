from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_add_cost_price_at_move'),
    ]

    operations = [
        # Update movement_type choices to include 'scrap'
        migrations.AlterField(
            model_name='stockmovement',
            name='movement_type',
            field=models.CharField(
                max_length=16,
                choices=[
                    ('receipt', 'Receção'),
                    ('delivery', 'Expedição'),
                    ('adjustment', 'Ajuste'),
                    ('scrap', 'Sucata'),
                ],
                verbose_name='Tipo de Movimento',
            ),
        ),
        # Add scrap_reason field
        migrations.AddField(
            model_name='stockmovement',
            name='scrap_reason',
            field=models.CharField(
                max_length=16,
                choices=[
                    ('damage',   'Avaria'),
                    ('expiry',   'Validade expirada'),
                    ('breakage', 'Quebra'),
                    ('quality',  'Controlo de qualidade'),
                    ('other',    'Outro'),
                ],
                null=True,
                blank=True,
                verbose_name='Motivo de Sucata',
                help_text='Apenas para movimentos de sucata.',
            ),
        ),
    ]
