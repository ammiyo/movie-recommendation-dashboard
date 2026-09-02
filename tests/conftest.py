import os
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

# The CSV dashboard does not need MySQL. Stub the optional connector so tests
# can import analytics_engine without mysql-connector-python installed.
if "mysql.connector" not in sys.modules:
    mysql = types.ModuleType("mysql")
    connector = types.ModuleType("mysql.connector")
    connector.Error = type("Error", (Exception,), {})
    connector.connect = lambda **kwargs: None
    mysql.connector = connector
    sys.modules["mysql"] = mysql
    sys.modules["mysql.connector"] = connector


import pytest

from analytics import analytics_engine as engine


@pytest.fixture(autouse=True)
def _reset_engine_cache():
    engine._cache.clear()
    yield
    engine._cache.clear()


@pytest.fixture()
def client():
    from app import app

    app.config["TESTING"] = True
    return app.test_client()
