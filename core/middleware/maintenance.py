from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from core.models import SiteSettings


class MaintenanceMiddleware(MiddlewareMixin):
    """
    Middleware для режима обслуживания сайта
    Проверяет настройки сайта и показывает страницу обслуживания если режим включен
    """
    
    def process_request(self, request):
        # Исключения для админки и статических файлов
        if request.path.startswith('/admin/') or \
           request.path.startswith('/static/') or \
           request.path.startswith('/media/'):
            return None
        
        try:
            settings = SiteSettings.get_settings()
            print(f"DEBUG: Maintenance mode = {settings.maintenance_mode}")  # Отладка
            
            if settings.maintenance_mode:
                print("DEBUG: Показываем страницу обслуживания")  # Отладка
                # Показываем страницу обслуживания
                context = {
                    'site_name': settings.site_name,
                    'maintenance_message': settings.maintenance_message or 'Сайт временно находится на техническом обслуживании. Пожалуйста, попробуйте зайти позже.',
                    'request': request,  # Добавляем request в контекст
                }
                
                # Создаем простой HTML ответ без сложного шаблона
                html_content = f"""
                <!DOCTYPE html>
                <html lang="ru">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Техническое обслуживание - {settings.site_name}</title>
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
                    <style>
                        body {{
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            min-height: 100vh;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                        }}
                        .maintenance-card {{
                            background: white;
                            border-radius: 20px;
                            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                            max-width: 500px;
                            width: 100%;
                            margin: 20px;
                        }}
                        .maintenance-icon {{
                            font-size: 4rem;
                            color: #667eea;
                        }}
                    </style>
                </head>
                <body>
                    <div class="maintenance-card p-5 text-center">
                        <div class="mb-4">
                            <i class="bi bi-tools maintenance-icon"></i>
                        </div>
                        
                        <h1 class="h2 mb-4 text-primary">Техническое обслуживание</h1>
                        
                        <div class="mb-4">
                            <p class="lead text-muted">{settings.maintenance_message}</p>
                        </div>
                        
                        <div class="row text-center">
                            <div class="col-md-4">
                                <i class="bi bi-clock text-info mb-2" style="font-size: 2rem;"></i>
                                <p class="small text-muted">Скоро вернемся</p>
                            </div>
                            <div class="col-md-4">
                                <i class="bi bi-shield-check text-success mb-2" style="font-size: 2rem;"></i>
                                <p class="small text-muted">Улучшаем сервис</p>
                            </div>
                            <div class="col-md-4">
                                <i class="bi bi-heart text-danger mb-2" style="font-size: 2rem;"></i>
                                <p class="small text-muted">Заботимся о вас</p>
                            </div>
                        </div>
                        
                        <hr class="my-4">
                        
                        <p class="small text-muted">
                            Если у вас срочный вопрос, пожалуйста, напишите нам на 
                            <a href="mailto:{settings.contact_email}">{settings.contact_email}</a>
                        </p>
                        
                        <div class="mt-4">
                            <button onclick="location.reload()" class="btn btn-primary">
                                <i class="bi bi-arrow-clockwise me-2"></i>Обновить страницу
                            </button>
                        </div>
                    </div>

                    <script>
                        // Автоматическое обновление каждые 30 секунд
                        setTimeout(function() {{
                            location.reload();
                        }}, 30000);
                    </script>
                </body>
                </html>
                """
                
                from django.http import HttpResponse
                response = HttpResponse(html_content, content_type='text/html')
                response.status_code = 503  # Service Unavailable
                return response
        except Exception as e:
            print(f"DEBUG: Ошибка в maintenance middleware: {e}")  # Отладка
            # Если ошибка при получении настроек, продолжаем нормально
            pass
        
        return None