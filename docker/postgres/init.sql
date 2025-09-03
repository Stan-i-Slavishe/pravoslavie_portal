-- 🗄️ Православный портал - PostgreSQL Initialization
-- Создание пользователя и базы данных

-- Создание роли для приложения
CREATE ROLE pravoslavie_user WITH LOGIN PASSWORD 'your_secure_postgres_password_here';

-- Предоставление прав на создание БД (для миграций)
ALTER ROLE pravoslavie_user CREATEDB;

-- Создание основной базы данных
CREATE DATABASE pravoslavie_portal_db OWNER pravoslavie_user;

-- Подключение к базе данных
\c pravoslavie_portal_db;

-- Создание схемы для приложения
CREATE SCHEMA IF NOT EXISTS public;

-- Предоставление всех прав на схему
GRANT ALL ON SCHEMA public TO pravoslavie_user;
GRANT ALL PRIVILEGES ON DATABASE pravoslavie_portal_db TO pravoslavie_user;

-- Установка расширений для PostgreSQL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- для полнотекстового поиска
CREATE EXTENSION IF NOT EXISTS "unaccent"; -- для поиска без учета диакритики

-- 📊 Настройка поиска для русского языка
CREATE TEXT SEARCH CONFIGURATION russian_hunspell (COPY = russian);

-- 🔒 Создание индексов для производительности
-- (будут созданы после миграций Django)

-- 💬 Комментарии к базе данных
COMMENT ON DATABASE pravoslavie_portal_db IS 'Orthodox Christian Portal Database';

-- 📝 Логирование создания БД
DO $$
BEGIN
    RAISE NOTICE 'PostgreSQL database for Pravoslavie Portal initialized successfully!';
    RAISE NOTICE 'Database: pravoslavie_portal_db';
    RAISE NOTICE 'User: pravoslavie_user';
    RAISE NOTICE 'Extensions: uuid-ossp, pg_trgm, unaccent';
END $$;
