-- ==========================================
-- СОЗДАНИЕ POSTGRESQL БД ДЛЯ ПРОЕКТА
-- ==========================================
-- Выполните этот скрипт в psql под пользователем postgres

-- Создание базы данных
CREATE DATABASE pravoslavie_local_db
    WITH 
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    TEMPLATE = template0;

-- Создание пользователя
CREATE USER pravoslavie_user WITH PASSWORD 'local_strong_password_2024';

-- Предоставление прав на базу данных
GRANT ALL PRIVILEGES ON DATABASE pravoslavie_local_db TO pravoslavie_user;

-- Подключение к новой БД
\connect pravoslavie_local_db

-- Предоставление прав на схему public
GRANT CREATE ON SCHEMA public TO pravoslavie_user;
GRANT USAGE ON SCHEMA public TO pravoslavie_user;

-- Предоставление прав на все таблицы
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO pravoslavie_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO pravoslavie_user;

-- Установка прав по умолчанию для новых объектов
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO pravoslavie_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO pravoslavie_user;

-- Проверка созданных объектов
\l pravoslavie_local_db
\du pravoslavie_user

-- Сообщение об успешном выполнении
SELECT 'PostgreSQL база данных pravoslavie_local_db успешно создана!' as result;