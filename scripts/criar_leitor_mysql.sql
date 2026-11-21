-- Execute com usuario administrador e substitua a senha.
CREATE USER IF NOT EXISTS 'leitor'@'%' IDENTIFIED BY 'TROQUE_ESTA_SENHA';
GRANT SELECT, SHOW VIEW ON meubanco.* TO 'leitor'@'%';
