from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_add_product_supplier_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='min_stock',
            field=models.DecimalField(
                blank=True,
                decimal_places=3,
                default=0,
                max_digits=12,
                verbose_name='Stock Mínimo',
                help_text='Alerta quando o stock em mão cair abaixo deste valor.',
            ),
        ),
    ]
