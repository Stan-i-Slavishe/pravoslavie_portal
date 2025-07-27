#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
sys.path.append(r'E:\pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from books.models import Book

def create_test_pdf():
    """Создаем простой тестовый PDF"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        
        # Путь к тестовому PDF
        test_pdf_path = r'E:\pravoslavie_portal\media\books\files\test_yandeks_direkt.pdf'
        
        # Создаем директорию если не существует
        os.makedirs(os.path.dirname(test_pdf_path), exist_ok=True)
        
        # Создаем PDF
        c = canvas.Canvas(test_pdf_path, pagesize=letter)
        width, height = letter
        
        # Страница 1
        c.setFont("Helvetica-Bold", 24)
        c.drawString(100, height - 100, "Яндекс Директ")
        c.setFont("Helvetica", 16)
        c.drawString(100, height - 140, "Полное руководство по контекстной рекламе")
        c.drawString(100, height - 180, "Тестовая версия PDF файла")
        
        c.setFont("Helvetica", 12)
        c.drawString(100, height - 220, "Эта книга содержит полное руководство по работе")
        c.drawString(100, height - 240, "с Яндекс Директ - системой контекстной рекламы.")
        
        c.drawString(100, height - 280, "Содержание:")
        c.drawString(120, height - 300, "1. Введение в Яндекс Директ")
        c.drawString(120, height - 320, "2. Создание первой рекламной кампании")
        c.drawString(120, height - 340, "3. Настройка ключевых слов")
        c.drawString(120, height - 360, "4. Оптимизация объявлений")
        c.drawString(120, height - 380, "5. Аналитика и отчеты")
        
        c.showPage()
        
        # Страница 2
        c.setFont("Helvetica-Bold", 18)
        c.drawString(100, height - 100, "Глава 1. Введение в Яндекс Директ")
        c.setFont("Helvetica", 12)
        
        text = [
            "Яндекс Директ - это система контекстной рекламы,",
            "которая позволяет размещать объявления в поисковой",
            "выдаче Яндекса и на партнерских сайтах.",
            "",
            "Основные преимущества:",
            "• Быстрый запуск рекламных кампаний",
            "• Точное таргетирование аудитории", 
            "• Контроль бюджета и ставок",
            "• Детальная аналитика результатов",
            "",
            "Система работает по принципу аукциона - чем выше",
            "ставка и качество объявления, тем выше позиция",
            "в рекламной выдаче."
        ]
        
        y = height - 140
        for line in text:
            c.drawString(100, y, line)
            y -= 20
        
        c.showPage()
        
        # Страница 3
        c.setFont("Helvetica-Bold", 18)
        c.drawString(100, height - 100, "Глава 2. Создание кампании")
        c.setFont("Helvetica", 12)
        
        text2 = [
            "Для создания эффективной рекламной кампании",
            "необходимо выполнить следующие шаги:",
            "",
            "1. Определить цели рекламы",
            "2. Выбрать тип кампании",
            "3. Настроить географическое таргетирование",
            "4. Установить бюджет и стратегию ставок",
            "5. Создать группы объявлений",
            "",
            "Важно помнить, что качественная настройка",
            "кампании на начальном этапе сэкономит время",
            "и бюджет в дальнейшем."
        ]
        
        y = height - 140
        for line in text2:
            c.drawString(100, y, line)
            y -= 20
        
        c.save()
        
        print(f"✅ Тестовый PDF создан: {test_pdf_path}")
        return test_pdf_path
        
    except ImportError:
        print("❌ Для создания PDF нужна библиотека reportlab:")
        print("pip install reportlab")
        return None
    except Exception as e:
        print(f"❌ Ошибка создания PDF: {e}")
        return None

def update_book_file():
    """Обновляем путь к файлу в базе данных"""
    try:
        book = Book.objects.get(id=2)
        test_pdf_path = 'books/files/test_yandeks_direkt.pdf'
        
        # Обновляем путь к файлу
        book.file = test_pdf_path
        book.save()
        
        print(f"✅ Путь к файлу обновлен: {book.file.path}")
        print(f"✅ URL файла: {book.file.url}")
        
    except Book.DoesNotExist:
        print("❌ Книга с ID 2 не найдена")
    except Exception as e:
        print(f"❌ Ошибка обновления: {e}")

if __name__ == "__main__":
    print("=== СОЗДАНИЕ ТЕСТОВОГО PDF ===")
    
    # Создаем тестовый PDF
    pdf_path = create_test_pdf()
    
    if pdf_path:
        # Обновляем запись в БД
        update_book_file()
        print("\n✅ Готово! Теперь можно тестировать PDF читалку.")
    else:
        print("\n❌ Не удалось создать тестовый PDF")
