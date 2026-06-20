from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0020_product_price_precision'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='conversion_loss_pct',
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                help_text='Percentagem de perda ao converter da UdM de compra para a UdM de stock. Ex: 10% — compra 1 kg, entram 900 g em stock (UdM principal).',
                max_digits=5,
                verbose_name='Perda na Conversão (%)',
            ),
        ),
    ]
