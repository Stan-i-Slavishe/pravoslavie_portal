# Generated migration for adding address and work hours fields to SiteSettings

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_add_mobile_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='work_hours',
            field=models.CharField(default='Пн-Пт: 9:00 - 18:00', help_text='Например: Пн-Пт: 9:00 - 18:00', max_length=100, verbose_name='Время работы'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='work_hours_note',
            field=models.CharField(blank=True, default='По московскому времени', max_length=50, verbose_name='Примечание к времени работы'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='address_city',
            field=models.CharField(default='г. Москва', max_length=100, verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='address_country',
            field=models.CharField(default='Россия', max_length=50, verbose_name='Страна'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='address_full',
            field=models.TextField(blank=True, help_text='Полный почтовый адрес (необязательно)', verbose_name='Полный адрес'),
        ),
    ]
