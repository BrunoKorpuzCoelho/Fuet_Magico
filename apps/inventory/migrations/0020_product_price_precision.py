from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0019_add_is_manufactured'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cost_price',
            field=models.DecimalField(
                decimal_places=6,
                default=0,
                help_text='Custo unitário em € por unidade de stock (UdM principal). Ex: 0,002000 €/g.',
                max_digits=14,
                verbose_name='Preço de Custo',
            ),
        ),
        migrations.AlterField(
            model_name='product',
            name='sale_price',
            field=models.DecimalField(
                decimal_places=6,
                default=0,
                help_text='Preço de venda em € por unidade de stock (UdM principal). Ex: 0,005000 €/g.',
                max_digits=14,
                verbose_name='Preço de Venda',
            ),
        ),
    ]
