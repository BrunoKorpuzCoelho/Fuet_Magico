# Generated migration — adds default_body_path to EmailTemplate
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_email_template_type_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailtemplate',
            name='default_body_path',
            field=models.CharField(
                blank=True,
                default='',
                help_text=(
                    'Caminho relativo dentro de templates/emails/ para o '
                    'ficheiro default do body. Ex: defaults/crm_thankyou.html. '
                    'Vazio = sem default (template personalizado).'
                ),
                max_length=255,
                verbose_name='Ficheiro default do body',
            ),
        ),
    ]
