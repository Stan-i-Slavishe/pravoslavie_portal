import ast
import sys

try:
    with open('E:/pravoslavie_portal/stories/views.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Попробуем парсить файл
    ast.parse(content)
    print("✅ Синтаксических ошибок не найдено!")
    
except SyntaxError as e:
    print(f"❌ Синтаксическая ошибка:")
    print(f"Строка {e.lineno}: {e.text}")
    print(f"Ошибка: {e.msg}")
    
    # Покажем контекст
    lines = content.split('\n')
    start = max(0, e.lineno - 6)
    end = min(len(lines), e.lineno + 5)
    
    print("\nКонтекст:")
    for i in range(start, end):
        marker = " --> " if i + 1 == e.lineno else "     "
        print(f"{marker}{i + 1:3}: {lines[i]}")

except Exception as e:
    print(f"Ошибка чтения файла: {e}")
