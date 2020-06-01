"""
The app fixture will call the factory and pass test_config to configure the
application and database for testing instead of using your local development
configuration.
"""

import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

## Load the SQL test cases we hard-coded in data.sql
with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    """
    Sets up an app
    """
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

