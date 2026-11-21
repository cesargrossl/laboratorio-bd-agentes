import importlib.util
from pathlib import Path
import pytest
spec = importlib.util.spec_from_file_location('mcp_server', Path(__file__).resolve().parents[1] / 'mcp' / 'server.py')
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)
@pytest.mark.parametrize('sql', ['DELETE FROM clientes', 'DROP TABLE clientes', 'SELECT * FROM clientes; DELETE FROM clientes', 'SELECT * INTO nova FROM clientes'])
def test_rejeita_escrita(sql):
    with pytest.raises(ValueError): server.validar_select(sql)
def test_aceita_select():
    assert server.validar_select('SELECT nome FROM clientes').startswith('SELECT')
