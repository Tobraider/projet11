import pytest
import sys
sys.path.append("..")

from server import app

@pytest.fixture
def client():
    app_test = app
    client_test = app_test.test_client()
    # with app_test.test_client as client:
    yield client_test

@pytest.fixture
def connecte(client):
    email = 'john@simplylift.co'
    reponse = client.post('/showSummary', data={'email':email})
    assert reponse.status_code == 302
    yield client