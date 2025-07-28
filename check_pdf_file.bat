@echo off
echo ========================================
echo       PDF DIAGNOSTICS
echo ========================================
echo.

call .venv\Scripts\activate

python -c "
import os
from books.models import Book

# Проверяем книгу Яндекс Директ
try:
    book = Book.objects.get(slug='yandeks-direkt')
    print(f'Book found: {book.title}')
    print(f'Format: {book.format}')
    print(f'Has file: {bool(book.file)}')
    if book.file:
        print(f'File path: {book.file.path}')
        print(f'File URL: {book.file.url}')
        print(f'File exists: {os.path.exists(book.file.path)}')
        if os.path.exists(book.file.path):
            print(f'File size: {os.path.getsize(book.file.path)} bytes')
    else:
        print('No file attached to book')
except Exception as e:
    print(f'Error: {e}')
"

echo.
echo Press any key to continue...
pause > nul
