# ==========================================
# 🔧 ИСПРАВЛЕНИЕ CSP ДЛЯ YOUTUBE IFRAME
# ==========================================

import re

# Читаем текущий файл
with open('E:/pravoslavie_portal/config/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Находим секцию CSP и добавляем frame-src
csp_pattern = r"(CSP_DEFAULT_SRC = ['\"]self['\"])"

# Если CSP настройки найдены
if 'CSP_DEFAULT_SRC' in content:
    print("✅ Найдены CSP настройки, добавляем frame-src для YouTube...")
    
    # Добавляем или обновляем frame-src после других CSP настроек
    if 'CSP_FRAME_SRC' in content:
        # Обновляем существующую
        content = re.sub(
            r'CSP_FRAME_SRC = ["\'][^"\']*["\']',
            'CSP_FRAME_SRC = "\'self\' https://www.youtube.com https://youtube.com"',
            content
        )
        print("🔄 Обновлена существующая CSP_FRAME_SRC")
    else:
        # Добавляем новую строку после CSP_CONNECT_SRC
        content = re.sub(
            r'(CSP_CONNECT_SRC = ["\'][^"\']*["\'])',
            r'\1\nCSP_FRAME_SRC = "\'self\' https://www.youtube.com https://youtube.com"',
            content
        )
        print("➕ Добавлена новая CSP_FRAME_SRC")
else:
    print("❌ CSP настройки не найдены!")

# Записываем обновленный файл
with open('E:/pravoslavie_portal/config/settings.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ CSP настройки обновлены!")
print("🎯 Теперь YouTube iframe должен работать!")
