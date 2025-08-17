# Emergency migration to add discount fields
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_purchase_download_count_purchase_last_downloaded'),
    ]

    operations = [
        # Используем RunSQL для прямого выполнения SQL команд
        migrations.RunSQL(
            """
            ALTER TABLE shop_order ADD COLUMN discount_amount DECIMAL(10,2) DEFAULT 0.00;
            """,
            reverse_sql="ALTER TABLE shop_order DROP COLUMN discount_amount;"
        ),
        migrations.RunSQL(
            """
            ALTER TABLE shop_order ADD COLUMN discount_code VARCHAR(50) DEFAULT '';
            """,
            reverse_sql="ALTER TABLE shop_order DROP COLUMN discount_code;"
        ),
    ]
