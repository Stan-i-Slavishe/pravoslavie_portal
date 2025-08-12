#!/usr/bin/env python
"""
SEO TEMPLATES CHECKER
====================
Проверка шаблонов на наличие SEO элементов
"""

import os
import sys
import django
from pathlib import Path
import re

# Настройка Django
PROJECT_ROOT = Path(r'E:\pravoslavie_portal')
sys.path.append(str(PROJECT_ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Ошибка настройки Django: {e}")
    sys.exit(1)

class TemplatesSEOChecker:
    def __init__(self):
        self.templates_dir = PROJECT_ROOT / 'templates'
        self.issues = []
        self.checked_templates = 0
        
    def check_template_file(self, template_path):
        """Проверка одного шаблона"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            relative_path = template_path.relative_to(self.templates_dir)
            issues = []
            
            # Проверки базового шаблона
            if template_path.name == 'base.html':
                if '{% block title %}' not in content:
                    issues.append("Отсутствует блок title")
                if '{% block meta_tags %}' not in content:
                    issues.append("Отсутствует блок meta_tags")
                if '{% block schema_ld %}' not in content:
                    issues.append("Отсутствует блок schema_ld")
                if '<meta name="viewport"' not in content:
                    issues.append("Отсутствует meta viewport")
                if 'canonical' not in content.lower():
                    issues.append("Отсутствует canonical URL")
            
            # Проверки детальных страниц
            elif '_detail.html' in template_path.name:
                if '{% load seo_tags %}' not in content:
                    issues.append("Не загружены seo_tags")
                if '{% render_meta_tags' not in content and '{% block meta_tags %}' not in content:
                    issues.append("Отсутствуют мета-теги")
                if '{% schema_ld' not in content and '{% block schema_ld %}' not in content:
                    issues.append("Отсутствует Schema.org")
                if 'og:' not in content and '{% render_meta_tags' not in content:
                    issues.append("Отсутствуют OpenGraph теги")
            
            # Проверки списковых страниц
            elif '_list.html' in template_path.name:
                if '{% load seo_tags %}' not in content:
                    issues.append("Не загружены seo_tags")
                if 'title' not in content.lower():
                    issues.append("Возможно отсутствует title")
            
            if issues:
                self.issues.append({
                    'template': str(relative_path),
                    'issues': issues
                })
                print(f"   ⚠️  {relative_path}: {len(issues)} проблем")
                for issue in issues:
                    print(f"      └─ {issue}")
            else:
                print(f"   ✅ {relative_path}")
                
            self.checked_templates += 1
            
        except Exception as e:
            print(f"   💥 Ошибка проверки {template_path}: {e}")
    
    def check_all_templates(self):
        """Проверка всех шаблонов"""
        print("🔍 Проверка SEO в шаблонах...")
        print("-" * 50)
        
        if not self.templates_dir.exists():
            print(f"❌ Папка шаблонов не найдена: {self.templates_dir}")
            return False
        
        # Найти все HTML файлы
        html_files = list(self.templates_dir.rglob('*.html'))
        
        if not html_files:
            print("❌ HTML шаблоны не найдены")
            return False
        
        print(f"📋 Найдено {len(html_files)} шаблонов для проверки\n")
        
        for template_file in html_files:
            self.check_template_file(template_file)
        
        return True
    
    def generate_report(self):
        """Генерация отчета по шаблонам"""
        print("\n" + "=" * 80)
        print("📊 ОТЧЕТ ПО SEO В ШАБЛОНАХ")
        print("=" * 80)
        
        if not self.issues:
            print("🎉 Все проверенные шаблоны соответствуют SEO требованиям!")
        else:
            print(f"⚠️  Найдено проблем в {len(self.issues)} шаблонах из {self.checked_templates}:\n")
            
            for issue_data in self.issues:
                print(f"📄 {issue_data['template']}:")
                for issue in issue_data['issues']:
                    print(f"   └─ {issue}")
                print()
        
        success_rate = ((self.checked_templates - len(self.issues)) / self.checked_templates) * 100 if self.checked_templates > 0 else 0
        
        print(f"📈 СТАТИСТИКА ШАБЛОНОВ:")
        print(f"   Проверено: {self.checked_templates}")
        print(f"   Без проблем: {self.checked_templates - len(self.issues)}")
        print(f"   С проблемами: {len(self.issues)}")
        print(f"   Успешность: {success_rate:.1f}%")

def main():
    """Главная функция"""
    print("🔍 SEO TEMPLATES CHECKER")
    print("🎯 Проверка шаблонов на SEO соответствие")
    print("=" * 50)
    
    checker = TemplatesSEOChecker()
    
    if checker.check_all_templates():
        checker.generate_report()
    else:
        print("❌ Не удалось проверить шаблоны")

if __name__ == '__main__':
    main()
