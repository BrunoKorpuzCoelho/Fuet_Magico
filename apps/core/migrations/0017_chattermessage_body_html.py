from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_chattermessage_bcc_emails'),
    ]

    operations = [
        migrations.AddField(
            model_name='chattermessage',
            name='body_html',
            field=models.TextField(blank=True, default='', verbose_name='Body HTML'),
        ),
    ]
