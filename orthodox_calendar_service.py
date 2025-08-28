#!/usr/bin/env python
"""
Сервис для получения православного календаря из внешних источников
"""

import requests
import json
from datetime import datetime, date
from typing import List, Dict, Optional

class OrthodoxCalendarService:
    """Сервис для работы с православным календарем"""
    
    def __init__(self):
        # API endpoints (примеры)
        self.apis = {
            'pravoslavie': 'https://pravoslavie.ru/api/calendar',
            'azbyka': 'https://azbyka.ru/api/calendar', 
            'calapi': 'https://calapi.ru/api/orthodox',
            # Резервные источники
            'local': 'local_calendar.json'
        }
    
    def get_events_for_date(self, target_date: date) -> List[Dict]:
        """Получить события на конкретную дату"""
        events = []
        
        # Пробуем разные источники
        for source_name, api_url in self.apis.items():
            try:
                if source_name == 'local':
                    events = self._get_local_events(target_date)
                else:
                    events = self._get_api_events(api_url, target_date)
                
                if events:
                    print(f"✅ Получены события из {source_name}")
                    break
                    
            except Exception as e:
                print(f"❌ Ошибка {source_name}: {e}")
                continue
        
        return events
    
    def _get_api_events(self, api_url: str, target_date: date) -> List[Dict]:
        """Получить события из внешнего API"""
        params = {
            'date': target_date.strftime('%Y-%m-%d'),
            'format': 'json'
        }
        
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return self._normalize_events(data)
    
    def _get_local_events(self, target_date: date) -> List[Dict]:
        """Получить события из локального файла"""
        # Базовые события (заглушка)
        local_events = {
            '01-07': [{'title': 'Рождество Христово', 'type': 'great_feast'}],
            '01-19': [{'title': 'Крещение Господне', 'type': 'great_feast'}],
            '02-15': [{'title': 'Сретение Господне', 'type': 'great_feast'}],
            '04-07': [{'title': 'Благовещение', 'type': 'great_feast'}],
            '08-19': [{'title': 'Преображение Господне', 'type': 'great_feast'}],
            '08-28': [{'title': 'Успение Пресвятой Богородицы', 'type': 'great_feast'}],
            '09-21': [{'title': 'Рождество Пресвятой Богородицы', 'type': 'great_feast'}],
            '09-27': [{'title': 'Воздвижение Креста Господня', 'type': 'great_feast'}],
            '12-04': [{'title': 'Введение во храм Пресвятой Богородицы', 'type': 'great_feast'}],
            '12-19': [{'title': 'День святителя Николая Чудотворца', 'type': 'saint'}],
        }
        
        date_key = target_date.strftime('%m-%d')
        return local_events.get(date_key, [])
    
    def _normalize_events(self, raw_data) -> List[Dict]:
        """Нормализация данных из разных источников"""
        # Здесь можно добавить логику для обработки разных форматов API
        if isinstance(raw_data, list):
            return raw_data
        elif isinstance(raw_data, dict) and 'events' in raw_data:
            return raw_data['events']
        else:
            return []

# Простой тест
def test_calendar_service():
    """Тестирование сервиса"""
    service = OrthodoxCalendarService()
    
    # Тестируем на разные даты
    test_dates = [
        date(2024, 1, 7),   # Рождество
        date(2024, 1, 19),  # Крещение
        date(2024, 12, 19), # Николай Чудотворец
        date.today(),       # Сегодня
    ]
    
    for test_date in test_dates:
        print(f"\n📅 Проверяем {test_date}:")
        events = service.get_events_for_date(test_date)
        
        if events:
            for event in events:
                print(f"  🕊️ {event.get('title', 'Без названия')}")
        else:
            print("  📖 Обычный день")

if __name__ == '__main__':
    print("🔔 Тестирование православного календаря...")
    test_calendar_service()
