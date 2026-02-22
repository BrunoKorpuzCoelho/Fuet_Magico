from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_chattermessage_direction_chattermessage_from_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chattermessage',
            name='bcc_emails',
            field=models.TextField(
                blank=True,
                verbose_name='BCC',
                help_text='Comma-separated email addresses (blind carbon copy)',
            ),
        ),
    ]
