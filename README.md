# Laboratorio de Banco de Dados I e II com agentes de IA

Projeto didatico com cinco SGBDs no Docker, Codex no VS Code, AGENTS.md, seis skills e servidor MCP para consultas de leitura.

## Requisitos
- Docker Engine + Docker Compose V2 (Docker Desktop no Windows)
- VS Code + extensao oficial **Codex – OpenAI's coding agent**; cada aluno usa sua propria conta conforme plano/limites
- Python 3.11+ para o MCP, Git e acesso ao modelo Codex pela internet
- Memoria e disco suficientes para **cinco SGBDs simultaneos**, especialmente Oracle e SQL Server

## Inicializacao
1. Copie `.env.example` para `.env` e substitua TODAS as senhas. Nao use senhas do ambiente anterior; se ja foram expostas, altere-as.
2. Execute `docker compose config` para validar o arquivo.
3. Execute `docker compose up -d` e `docker compose ps`.
4. PostgreSQL e MySQL executam scripts de `db/*` **apenas quando o volume de dados esta vazio**. Em volumes existentes, execute scripts manualmente e com backup.
5. Abra a pasta do projeto no VS Code e autentique a extensao Codex.
6. Peça ao agente: `Leia AGENTS.md e me ajude na atividade exercicios/aula01 sem entregar a solucao.`

## MCP — conexao real com bancos
O MCP e opcional. Ele NAO esta dentro do Docker; roda localmente no computador do aluno, no VS Code, e conecta aos bancos autorizados.

### Windows (PowerShell)
```
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r mcp/requirements.txt
```
Copie `mcp/mcp-windows.json` para `.vscode/mcp.json` no Windows. Em Linux/macOS use o arquivo `.vscode/mcp.json` ja incluido e `python3 -m venv .venv && .venv/bin/pip install -r mcp/requirements.txt`.

Crie usuarios **somente leitura** nos bancos que serao consultados (scripts de exemplo em `scripts/` para PostgreSQL e MySQL). Atualize `MCP_PG_URL` e/ou `MCP_MYSQL_URL` em `.env` com esses usuarios; as linhas com `SENHA` sao placeholders e nao conectam. Para SQL Server/Oracle, configure contas read-only e drivers no host; os exemplos de URL em `.env.example` precisam ser adaptados e testados. Para MongoDB, crie conta com papel `read` e informe `MCP_MONGO_URI`.

No VS Code, habilite o servidor MCP configurado e autorize suas ferramentas no agente quando solicitado. Ferramentas: `bancos_disponiveis`, `listar_tabelas`, `descrever_tabela`, `executar_select`, `listar_colecoes_mongo`. O MongoDB nesta versao expoe apenas listagem de colecoes; nao executa consultas Mongo.

**Seguranca**: a verificacao textual de SELECT e apenas uma barreira adicional; nao e um parser SQL de seguranca. O limite de 50 linhas limita a resposta, nao necessariamente o trabalho executado pelo banco. Use obrigatoriamente usuario read-only, timeout de consulta, bancos separados por equipe, rede restrita e dados ficticios. Nao exponha portas dos SGBDs na rede sem controles adicionais. O Compose publica somente em `127.0.0.1`, adequado para uso local. Para servidor central, configure rede, firewall, TLS/VPN, credenciais por equipe e politicas institucionais.

## Testes
```
.venv\Scripts\python.exe -m pip install pytest
.venv\Scripts\python.exe -m pytest -q
```

## Observacoes de compatibilidade
- O `version: "3"` foi removido por ser obsoleto no Compose V2.
- SQL Server 2019 nao interpreta automaticamente `/docker-entrypoint-initdb.d`.
- Oracle XE 21c usa `XEPDB1` como service name; `ORACLE_DATABASE` nao e usado aqui.
- MongoDB 4.4 foi mantido para compatibilidade, mas e antigo e pode falhar em CPUs modernas. Planeje atualizacao testada.
- Em Linux com SELinux e em Macs ARM, pode ser necessario adaptar volumes/imagens.
- Codex usa servico OpenAI; este pacote nao inclui modelo local nem uso ilimitado gratuito.

## Roteiro didatico
- Aula 1: SELECT, filtros e verificacao de respostas da IA.
- Aula 2: DER, PK/FK, JOIN e validacao com MCP.
- Aula 3: normalizacao e anomalias.
- Aula 4: indices e planos de execucao.
- Aula 5: CRUD e testes em banco de exercicios autorizado.
- Projeto final: oficina mecanica (ver `exercicios/projeto-final`).

## Avaliacao e integridade academica
Exigir SQL original, explicacao de escolhas, evidencias dos testes e registro do uso da IA. Professor define quando permitir solucao completa. Nao compartilhar contas nem segredos. Skills em `.agents/skills/` orientam tarefas; a disponibilidade de descoberta automatica depende da versao do Codex.
