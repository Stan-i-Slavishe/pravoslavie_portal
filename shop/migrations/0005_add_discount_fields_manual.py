# Manual migration for discount fields in Order model
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_purchase_download_count_purchase_last_downloaded'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discount_amount',
            field=models.DecimalField(decimal_places=2, default=0.00, max_digits=10, verbose_name='Размер скидки'),
        ),
        migrations.AddField(
            model_name='order',
            name='discount_code',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Промокод'),
        ),
    ]
