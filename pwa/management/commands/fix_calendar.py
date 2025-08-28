from django.core.management.base import BaseCommand
from pwa.models import DailyOrthodoxInfo
from datetime import date

class Command(BaseCommand):
    help = 'Быстрое исправление данных православного календаря'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🔧 Исправляем данные православного календаря...')
        )

        # Исправляем 21 августа
        daily_info, created = DailyOrthodoxInfo.objects.get_or_create(
            month=8,
            day=21
        )
        
        daily_info.fasting_type = 'strict_fast'
        daily_info.fasting_description = 'Успенский пост: горячая пища без масла'
        daily_info.allowed_food = '''🍲 <strong>Успенский пост - горячее без масла:</strong>

✅ <strong>Разрешается:</strong>
• Каши на воде: гречневая, овсяная, рисовая, пшенная
• Постные супы: овощные, грибные, щи постные
• Отварные овощи: картофель, морковь, свекла, капуста
• Картофель печеный в мундире
• Тушеные овощи без масла
• Грибы отварные, тушеные (без масла)
• Бобовые: горох, фасоль, чечевица
• Макароны (из твердых сортов пшеницы)
• Компоты из свежих фруктов
• Чай, кофе, травяные отвары

❌ <strong>Запрещается:</strong>
• Растительное масло для готовки
• Жареная пища
• Продукты животного происхождения
• Сливочное масло

💡 <strong>Рецепт:</strong> Овощное рагу без масла - тушите овощи в собственном соку'''
        
        daily_info.spiritual_note = 'Горячая пища без масла. Время умеренности и духовного сосредоточения.'
        daily_info.save()
        
        action = "Создана" if created else "Обновлена"
        self.stdout.write(
            self.style.SUCCESS(f'✅ {action} запись для 21 августа: {daily_info.get_fasting_type_display()}')
        )

        self.stdout.write(
            self.style.SUCCESS('✅ Данные исправлены! Обновите страницу в браузере.')
        )
