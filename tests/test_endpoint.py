import requests


def test_recommendations():
    response = requests.get('http://localhost:80/recommendations?user_id=18')
    assert response.status_code == 200
    data = response.json()
    assert list(data.keys()) == ['items']
    assert len(data['items']) == 2
    for item in data['items']:
        assert list(item.keys()) == ['id']


def test_recommendations_with_metadata():
    response = requests.get('http://localhost:80/recommendations?user_id=18&returnMetadata=true')
    assert response.status_code == 200
    data = response.json()
    assert list(data.keys()) == ['items']
    assert len(data['items']) == 2
    for item in data['items']:
        assert sorted(list(item.keys())) == sorted(['id', 'title', 'genres'])


def test_features():
    response = requests.get('http://localhost:80/features?user_id=18')
    assert response.status_code == 200
    data = response.json()
    assert list(data.keys()) == ['features']
    assert len(data['features']) == 1
    assert list(data['features'][0].keys()) == ['histories']
    assert 185135 in data['features'][0]['histories']
    assert 180777 in data['features'][0]['histories']
    assert 180095 in data['features'][0]['histories']
    assert 177593 in data['features'][0]['histories']
