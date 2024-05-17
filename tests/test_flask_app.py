from app.main import app
import pytest


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_recommendations(client):
    response = client.get('/recommendations?user_id=18')
    assert response.status_code == 200
    assert list(response.json.keys()) == ['items']
    assert len(response.json['items']) == 2
    for item in response.json['items']:
        assert list(item.keys()) == ['id']


def test_recommendations_with_metadata(client):
    response = client.get('/recommendations?user_id=18&returnMetadata=true')
    assert response.status_code == 200
    assert list(response.json.keys()) == ['items']
    assert len(response.json['items']) == 2
    for item in response.json['items']:
        assert sorted(list(item.keys())) == sorted(['id', 'title', 'genres'])


def test_features(client):
    response = client.get('/features?user_id=18')
    assert response.status_code == 200
    assert list(response.json.keys()) == ['features']
    assert len(response.json['features']) == 1
    assert list(response.json['features'][0].keys()) == ['histories']
    assert 185135 in response.json['features'][0]['histories']
    assert 180777 in response.json['features'][0]['histories']
    assert 180095 in response.json['features'][0]['histories']
    assert 177593 in response.json['features'][0]['histories']

