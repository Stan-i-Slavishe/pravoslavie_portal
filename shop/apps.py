from django.apps import AppConfig

class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
    verbose_name = 'Интернет-магазин'
    
    def ready(self):
        """Импортируем сигналы при инициализации приложения для автоматической синхронизации"""
        import shop.signals
