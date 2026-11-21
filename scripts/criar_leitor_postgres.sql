-- Execute com usuario administrador NO BANCO DE EXERCICIOS, apos ajustar a senha.
CREATE ROLE leitor LOGIN PASSWORD 'TROQUE_ESTA_SENHA';
GRANT CONNECT ON DATABASE meubanco TO leitor;
GRANT USAGE ON SCHEMA public TO leitor;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO leitor;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO leitor;
ALTER ROLE leitor SET statement_timeout = '5s';
