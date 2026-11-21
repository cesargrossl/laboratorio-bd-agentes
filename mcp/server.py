"""MCP stdio para metadados e SELECT restrito. Configure credenciais read-only.
Aviso: validacao SQL por texto nao substitui permissoes do banco e isolamento.
"""
import os
import re
from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import URL
import sqlparse

load_dotenv(Path(__file__).resolve().parents[1] / '.env')
mcp = FastMCP('laboratorio-bd')
URLS = {
    'postgres': os.getenv('MCP_PG_URL', ''),
    'mysql': os.getenv('MCP_MYSQL_URL', ''),
    'sqlserver': os.getenv('MCP_MSSQL_URL', ''),
    'oracle': os.getenv('MCP_ORACLE_URL', ''),
}

def engine_for(banco: str):
    if banco not in URLS or not URLS[banco] or 'SENHA' in URLS[banco]:
        raise ValueError('Banco nao configurado com credenciais de leitura: ' + banco)
    return create_engine(URLS[banco], pool_pre_ping=True, connect_args={})

@mcp.tool()
def bancos_disponiveis() -> list[str]:
    """Lista SGBDs com conexao MCP configurada."""
    configured = [k for k,v in URLS.items() if v and 'SENHA' not in v]
    if os.getenv('MCP_MONGO_URI') and 'SENHA' not in os.getenv('MCP_MONGO_URI', ''):
        configured.append('mongo')
    return configured

@mcp.tool()
def listar_tabelas(banco: str) -> list[str]:
    """Lista tabelas acessiveis em um SGBD relacional."""
    engine = engine_for(banco)
    try:
        return inspect(engine).get_table_names()
    finally:
        engine.dispose()

@mcp.tool()
def descrever_tabela(banco: str, tabela: str) -> dict:
    """Retorna colunas, PK e FKs de uma tabela existente."""
    engine = engine_for(banco)
    try:
        insp = inspect(engine)
        if tabela not in insp.get_table_names():
            raise ValueError('Tabela inexistente ou sem acesso')
        return {
            'colunas': [{'nome':c['name'], 'tipo':str(c['type']), 'nullable':c.get('nullable')} for c in insp.get_columns(tabela)],
            'pk': insp.get_pk_constraint(tabela),
            'fks': insp.get_foreign_keys(tabela),
        }
    finally:
        engine.dispose()

def validar_select(sql: str):
    # Defesa adicional; conta do banco DEVE ser exclusivamente leitura.
    statements = sqlparse.parse(sql)
    if len(statements) != 1:
        raise ValueError('Somente uma consulta por vez')
    stmt = statements[0]
    if stmt.get_type() != 'SELECT':
        raise ValueError('Somente SELECT e permitido')
    normalized = sqlparse.format(sql, strip_comments=True).strip()
    if not normalized.upper().startswith('SELECT '):
        raise ValueError('A consulta deve comecar por SELECT')
    if re.search(r'\b(INTO|FOR\s+UPDATE|OUTFILE|DUMPFILE|XP_CMDSHELL|DBMS_|PG_SLEEP|SLEEP|BENCHMARK)\b',normalized,re.I):
        raise ValueError('Construcao SQL nao permitida')
    return normalized

@mcp.tool()
def executar_select(banco: str, consulta: str) -> dict:
    """Executa SELECT com ate 50 linhas em banco relacional usando conta read-only."""
    sql = validar_select(consulta)
    engine = engine_for(banco)
    try:
        with engine.connect() as conn:
            # Timeout de consulta deve ser configurado no servidor/role do SGBD.
            result = conn.execute(text(sql))
            rows = [dict(row._mapping) for row in result.fetchmany(50)]
            return {'linhas':rows, 'limite_retorno':50, 'colunas':list(result.keys())}
    finally:
        engine.dispose()

@mcp.tool()
def listar_colecoes_mongo() -> list[str]:
    """Lista colecoes MongoDB com usuario read-only."""
    from pymongo import MongoClient
    uri = os.getenv('MCP_MONGO_URI', '')
    if not uri or 'SENHA' in uri:
        raise ValueError('Mongo nao configurado')
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    try:
        return client[os.getenv('MCP_MONGO_DB','meubanco')].list_collection_names()
    finally:
        client.close()

if __name__ == '__main__':
    mcp.run(transport='stdio')
