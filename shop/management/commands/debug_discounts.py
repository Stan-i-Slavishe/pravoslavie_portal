from django.core.management.base import BaseCommand
from shop.models import Cart, Discount
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Диагностика проблемы со скидками'

    def handle(self, *args, **options):
        self.stdout.write("🔍 ДИАГНОСТИКА ПРОБЛЕМЫ СО СКИДКАМИ")
        self.stdout.write("=" * 50)
        
        # 1. Проверяем структуру модели Cart
        self.stdout.write("\n1. ПРОВЕРКА МОДЕЛИ CART:")
        self.stdout.write("-" * 30)
        
        try:
            cart_fields = [field.name for field in Cart._meta.fields]
            self.stdout.write(f"✅ Поля модели Cart: {cart_fields}")
            
            if 'applied_discount_code' in cart_fields:
                self.stdout.write(self.style.SUCCESS("✅ Поле applied_discount_code найдено"))
            else:
                self.stdout.write(self.style.ERROR("❌ Поле applied_discount_code НЕ НАЙДЕНО - нужна миграция!"))
                
            if 'discount_amount' in cart_fields:
                self.stdout.write(self.style.SUCCESS("✅ Поле discount_amount найдено"))
            else:
                self.stdout.write(self.style.ERROR("❌ Поле discount_amount НЕ НАЙДЕНО - нужна миграция!"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Ошибка при проверке модели: {e}"))
        
        # 2. Создаем тестовый промокод
        self.stdout.write("\n2. СОЗДАНИЕ ТЕСТОВОГО ПРОМОКОДА:")
        self.stdout.write("-" * 30)
        
        try:
            test_code = "DEBUG15"
            
            if not Discount.objects.filter(code=test_code).exists():
                Discount.objects.create(
                    code=test_code,
                    description="Тестовый промокод для отладки",
                    discount_type='percentage',
                    discount_value=15,
                    min_amount=0,
                    valid_from=timezone.now(),
                    valid_until=timezone.now() + timedelta(days=30),
                    is_active=True
                )
                self.stdout.write(self.style.SUCCESS(f"✅ Создан тестовый промокод: {test_code}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"✅ Тестовый промокод {test_code} уже существует"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Ошибка при создании тестового промокода: {e}"))
        
        # 3. Проверяем корзины
        self.stdout.write("\n3. ПРОВЕРКА КОРЗИН:")
        self.stdout.write("-" * 30)
        
        try:
            carts = Cart.objects.all()
            self.stdout.write(f"Всего корзин: {carts.count()}")
            
            for cart in carts[:2]:
                self.stdout.write(f"  Корзина {cart.id} (пользователь: {cart.user.username})")
                try:
                    self.stdout.write(f"    - applied_discount_code: '{cart.applied_discount_code}'")
                    self.stdout.write(f"    - discount_amount: {cart.discount_amount}")
                    self.stdout.write(f"    - has_discount: {cart.has_discount}")
                except AttributeError as e:
                    self.stdout.write(self.style.ERROR(f"    ❌ Ошибка доступа к полю: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Ошибка при проверке корзин: {e}"))
        
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("📋 РЕКОМЕНДАЦИИ:")
        self.stdout.write("1. Если поля отсутствуют, выполните:")
        self.stdout.write("   python manage.py makemigrations shop --name add_discount_fields_to_cart")
        self.stdout.write("   python manage.py migrate shop")
        self.stdout.write("2. Используйте промокод DEBUG15 для тестирования")
