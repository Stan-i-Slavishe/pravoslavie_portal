# Manual migration to resolve dependency issues
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_add_discount_fields_to_order'),
    ]

    operations = [
        # Empty migration - fields already added in 0004
        # This migration exists only to satisfy dependency chain
    ]
