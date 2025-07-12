# playlist_state_manager.py - Простой менеджер состояния плейлистов

import os
import json
from django.conf import settings

class PlaylistStateManager:
    """Простой менеджер состояния плейлистов без моделей БД"""
    
    def __init__(self):
        self.state_file = os.path.join(settings.BASE_DIR, 'playlist_states.json')
        self.states = self.load_states()
    
    def load_states(self):
        """Загружает состояния из файла"""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}
    
    def save_states(self):
        """Сохраняет состояния в файл"""
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.states, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def get_user_state(self, user_id):
        """Получает состояние плейлистов пользователя"""
        return self.states.get(str(user_id), {})
    
    def set_story_in_playlist(self, user_id, story_slug, playlist_id, is_in_playlist):
        """Устанавливает состояние рассказа в плейлисте"""
        user_key = str(user_id)
        if user_key not in self.states:
            self.states[user_key] = {}
        
        if story_slug not in self.states[user_key]:
            self.states[user_key][story_slug] = {}
        
        self.states[user_key][story_slug][playlist_id] = is_in_playlist
        self.save_states()
    
    def is_story_in_playlist(self, user_id, story_slug, playlist_id):
        """Проверяет, находится ли рассказ в плейлисте"""
        user_state = self.get_user_state(user_id)
        return user_state.get(story_slug, {}).get(playlist_id, False)

# Глобальный экземпляр
playlist_manager = PlaylistStateManager()
